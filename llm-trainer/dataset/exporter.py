import json
from pathlib import Path
from dataset.builder import DatasetBuilder

class DatasetExporter:
    def __init__(self,poems_dir="data/raw/poems",output_dir="data/datasets"):
        self.poems_dir = Path(poems_dir)
        self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
        self.builder = DatasetBuilder()
    
    def export(self):
        print('start export')
        output_file = (
            self.output_dir /
            "mixed.jsonl"
        )
        
        count = 0
        
        with output_file.open(
            "w",
            encoding="utf-8"
        ) as writer:
            for poem_file in self.poems_dir.glob("*.json"):
                data = json.loads(
                    poem_file.read_text(
                        encoding="utf-8"
                    )
                )
                
                poem = data["processed"]
                samples = self.builder.build_all(
                    poem
                )
                
                for sample in samples:
                    writer.write(
                        json.dumps(
                            sample,
                            ensure_ascii=False
                        )
                    )
                    
                    writer.write("\n")
                    count += 1
                    
            print(f"exported {count} samples")
                