import sys

from crawlers.ganjoor import GanjoorCrawler
from crawlers.ganjoor_client import GanjoorClient
from storage.raw_storage import RawStorage
from storage.state_storage import StateStorage


def build_crawler():
    return GanjoorCrawler(
        GanjoorClient(),
        RawStorage(),
        StateStorage()
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <command>")
        print("Commands: crawl_all")
        return

    command = sys.argv[1]

    crawler = build_crawler()

    if command == "crawl_all":
        crawler.crawl_all()

    elif command == "crawl":
        crawler.crawl()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()