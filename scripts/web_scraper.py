from playwright.sync_api import sync_playwright

url = "https://www.cnbc.com/world/?region=world"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(url, timeout=60000)

    page.wait_for_selector(
        '#market-data-scroll-container a[class*="MarketCard-container"]', timeout=60000
    )
    html = page.content()

    browser.close()

with open("../data/raw_data/web_data.html", "w", encoding="utf-8") as f:
    f.write(html)
