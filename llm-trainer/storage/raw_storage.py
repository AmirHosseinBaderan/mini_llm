import json
from pathlib import Path

class RawStorage:
    def __init__(self,root="data/raw"):
        self.root = Path(root)
        
    def _get_path(self,collection:str,item_id:int)-> Path:
        directory = self.root / collection
        
        directory.mkdir(
            parents=True,
            exist_ok=True
        )
        
        return directory / f"{item_id}.json"
    
    def save(self,collection:str,item_id:int,data:dict):
        path = self._get_path(collection,item_id)
        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )
        )
        
    def load(self,collection:str,item_id:int)-> dict:
        path = self._get_path(collection,item_id)
        
        return json.loads(path.read_text(encoding="utf-8"))
    
    def exists(self,collection:str,item_id:int)-> bool:
        path = self._get_path(collection,item_id)
        return path.exists()