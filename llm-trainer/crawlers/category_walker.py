class CategoryWalker:
    def __init__(self,client,raw_storage):
        self.client = client
        self.raw_storage = raw_storage
        
    def walk(self,category_id):
        category = self.client.get_category(category_id)
        self.raw_storage.save(
            "categories",
            category_id,
            category
        )
        
        yield category
        
        for child in category["cat"]["children"]:
            yield from self.walk(
                child["id"]
            )