from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page()

    page.goto("https://app.rankedvote.co/rv/lamansion/vote")

    page.wait_for_selector("input[type='radio']")

    radio_buttons = page.query_selector_all("input[type='radio']")

    print("\n=== DATOS COMPLETOS DEL DOM ===\n")

    for rb in radio_buttons:
        info = {}

        # ID, VALUE, LABEL
        info["id"] = rb.get_attribute("id")
        info["value"] = rb.get_attribute("value")
        info["aria-label"] = rb.get_attribute("aria-label")

        # todos los atributos
        attrs = page.evaluate("""
            (el) => {
                const attr = {};
                for (let a of el.attributes) {
                    attr[a.name] = a.value;
                }
                return attr;
            }
        """, rb)
        info["attributes"] = attrs

        # HTML interno (del input)
        html = page.evaluate("(el) => el.outerHTML", rb)
        info["html"] = html

        # Buscar el label asociado
        label_selector = f"label[for='{info['id']}']"
        label = page.query_selector(label_selector)
        info["label_text"] = label.inner_text() if label else None
        info["label_html"] = page.evaluate("(el) => el.outerHTML", label) if label else None

        print(info)
        print("=" * 50)

    browser.close()
