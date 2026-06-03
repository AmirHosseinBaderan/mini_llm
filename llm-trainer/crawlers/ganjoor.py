from crawlers.http_client import HttpClient

class GanjoorCrawler:
    
    BASE_URL = (
        "https://api.ganjoor.net/api"
    )
    
    def __init__(self):
        self.http = HttpClient()
        
    def get_poets(self):
        return self.http.get(
            f"{self.BASE_URL}/ganjoor/poets"
        )