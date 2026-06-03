from crawlers.ganjoor import GanjoorCrawler

crawler = GanjoorCrawler()
poets = crawler.get_poets()

print(f"Poets count : {len(poets)}")

for poet in poets[:10]:
    print(poet)