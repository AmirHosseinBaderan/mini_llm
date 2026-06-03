from crawlers.ganjoor import GanjoorCrawler
from crawlers.ganjoor_client import GanjoorClient

from storage.raw_storage import RawStorage
from storage.state_storage import StateStorage


crawler = GanjoorCrawler(
    GanjoorClient(),
    RawStorage(),
    StateStorage()
)

crawler.crawl_all()