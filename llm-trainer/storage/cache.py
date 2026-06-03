import hashlib
import json
from pathlib import Path


class FileCache:
    def __init__(self,cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
    def _key_to_path(self,key):
        hashed = hashlib.sha256(
            key.encode()
        ).hexdigest()
        
        return self.cache_dir / f"{hashed}.json"
    
    def get(self,key):
        path = self._key_to_path(key)
        if not path.exists():
            return None
        
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
        
    def set(self,key,value):
        path = self._key_to_path(key)
        
        path.write_text(
            json.dumps(
                value,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )        