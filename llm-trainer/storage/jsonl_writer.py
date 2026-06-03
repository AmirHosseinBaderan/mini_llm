import json
from pathlib import Path 
from dataclasses import asdict

class JsonlWriter:

    def __init__(self,path:str):
        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
    
    def write(self,document):

        with open(
            self.path,
            "a",
            encoding="utf-8"
        ) as file:
            file.write(
                json.dumps(
                    asdict(document),
                    ensure_ascii=False
                )
            )
            file.write("\n")