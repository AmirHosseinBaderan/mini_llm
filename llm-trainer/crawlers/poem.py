
class PoemCrawler:
    def __init__(self,client,raw_storage):
        self.client = client
        self.raw_storage = raw_storage
        
    def crawl(self,poem_id:int):
        poem = self.client.get_poem(poem_id)
        
        self.raw_storage.save("poems",poem_id,poem)
        
        return poem