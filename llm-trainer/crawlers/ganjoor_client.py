from crawlers.http_client import HttpClient

class GanjoorClient:
    BASE_URL = "https://api.ganjoor.net/api"
    
    def __init__(self):
        self.http = HttpClient()
        
    def get_poets(self):
        return self.http.get(
            f"{self.BASE_URL}/ganjoor/poets"
        )
        
    def get_category(self,category_id):
        return self.http.get(
            f"{self.BASE_URL}/ganjoor/cat/{category_id}?poems=true&mainSections=false"
        )
        
    def get_poem(self,poem_id:int):
        return self.http.get(
            f"{self.BASE_URL}/ganjoor/poem/{poem_id}"
        )