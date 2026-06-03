from storage.raw_storage import RawStorage
from storage.state_storage import StateStorage
from processors.poem_processor import PoemProcessor


class GanjoorCrawler:

    def __init__(
        self,
        client,
        raw_storage: RawStorage,
        state_storage: StateStorage
    ):

        self.client = client
        self.raw_storage = raw_storage
        self.state_storage = state_storage
        self.processor = PoemProcessor()

        self.state = state_storage.load()

        self.state.setdefault(
            "poets_completed",
            []
        )
        
        self.state.setdefault(
            "categories_completed",
            []
        )
        
        self.state.setdefault(
            "poems_completed",
            []
        )
        
    def save_state(self):
        self.state_storage.save(
            self.state
        )
        
    def crawl_poem(self, poem_id: int):
        if poem_id in self.state["poems_completed"]:
            return
    
        poem = self.client.get_poem(poem_id)
        processed = self.processor.build(poem)
    
        self.raw_storage.save(
            "poems",
            poem_id,
            {
                "raw": poem,
                "processed": processed
            }
        )
    
        self.state["poems_completed"].append(poem_id)
    
        self.save_state()
        
    def crawl_category(
        self,
        category_id: int
    ):

        if category_id in self.state[
            "categories_completed"
        ]:
            return

        category = self.client.get_category(
            category_id
        )

        self.raw_storage.save(
            "categories",
            category_id,
            category
        )

        cat = category["cat"]

        for poem in cat["poems"]:
            self.crawl_poem(
                poem["id"]
            )

        for child in cat["children"]:
            self.crawl_category(
                child["id"]
            )

        self.state[
            "categories_completed"
        ].append(category_id)

        self.save_state()
   
    def crawl_poet(
        self,
        poet: dict
    ):

        poet_id = poet["id"]

        if poet_id in self.state[
            "poets_completed"
        ]:
            return

        self.raw_storage.save(
            "poets",
            poet_id,
            poet
        )

        self.crawl_category(
            poet["rootCatId"]
        )

        self.state[
            "poets_completed"
        ].append(poet_id)

        self.save_state()
        
    def crawl_all(self):

        poets = self.client.get_poets()

        for poet in poets:

            self.crawl_poet(
                poet
            )