import json
from pathlib import Path

class StateStorage:
    def __init__(self,path="state.json"):
        self.path = Path(path)
        
    def load(self):
        if not self.path.exists():
            return {}
        
        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )
        
    def save(self,state):
        self.path.write_text(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )