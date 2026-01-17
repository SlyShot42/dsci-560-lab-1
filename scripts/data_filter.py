from bs4 import BeautifulSoup
from pathlib import Path
import re
import csv

html_path = Path("../data/raw_data/web_data.html")

print(f"Reading HTML content from: {html_path}")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("Parsing market data cards...")
cards = soup.select("#market-data-scroll-container a.MarketCard-container")

print("Creating/overwriting market data CSV file...")
with open(
    "../data/processed_data/market_data.csv", "w", newline="", encoding="utf-8"
) as f:
    writer = csv.writer(f)
    writer.writerow(
        ["marketCard_symbol", "marketCard_stockPosition", "marketCard_changePct"]
    )
    print("Extracting and storing data from market cards into csv...")
    for card in cards:
        card_content = card.get_text(separator=" ", strip=True)

        match = re.search(
            r"^([A-Z][A-Z0-9\s]*)\*\s+([0-9]{1,3}(?:\,[0-9]{3})*(?:\.[0-9]+)?)\s+\w+\s+(?:[+-]?[0-9]{0,3}(?:\,[0-9]{3})*(?:\.[0-9]+)?)\s+([+-]?[0-9]{0,3}(?:\,[0-9]{3})*(?:\.[0-9]+)?\%)",
            card_content,
        )
        marketCard_symbol = match.group(1) if match else None
        marketCard_stockPosition = (
            float(match.group(2).replace(",", "")) if match else None
        )
        marketCard_changePct = (
            float(match.group(3).replace("%", "").replace(",", "")) if match else None
        )
        writer.writerow(
            [marketCard_symbol, marketCard_stockPosition, marketCard_changePct]
        )

print("Parsing latest news items...")
LatestNews_section = soup.select("ul.LatestNews-list > li.LatestNews-item")


print("Creating/overwriting latest news CSV file...")
with open(
    "../data/processed_data/news_data.csv", "w", newline="", encoding="utf-8"
) as f:
    writer = csv.writer(f)
    writer.writerow(["LatestNews_timestamp", "title", "link"])

    print("Extracting and storing data from latest news into csv...")
    for news_item in LatestNews_section:
        timestamp_container = news_item.select("time.LatestNews-timestamp")
        LatestNews_timestamp = (
            timestamp_container[0].get_text(separator=" ", strip=True)
            if timestamp_container
            else None
        )

        title_container = news_item.select("a.LatestNews-headline")
        title = (
            title_container[0].get_text(separator=" ", strip=True)
            if title_container
            else None
        )

        links = news_item.select("a.LatestNews-headline[href]")
        link = links[0]["href"] if links else None

        writer.writerow([LatestNews_timestamp, title, link])
