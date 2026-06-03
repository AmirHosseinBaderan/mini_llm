import sentencepiece as spm
from pathlib import Path
import json

class TokenizerTrainer:
    def __init__(self,dataset_path="data/datasets/mixed.jsonl",output_dir="tokenizer/vocab"):
        self.dataset_path = Path(dataset_path)
        self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
    def build_corpus(self):
        corpus_path = self.output_dir / "corpus.txt"
        
        with(
            open(self.dataset_path,"r",encoding="utf-8") as dataset,
            open(corpus_path,"w",encoding="utf-8") as corpus
        ):
            for line in dataset:
                doc = json.loads(line)
            
                if doc["type"] == "corpus":
                
                    text = doc["text"]
            
                elif doc["type"] == "instruction":
                
                    text = (
                        doc["instruction"]
                        + "\n"
                        + doc["input"]
                        + "\n"
                        + doc["output"]
                    )
            
                else:
                    continue
                
                text = text.replace("\n", " ")
            
                corpus.write(text + "\n")
                
            return corpus_path
    
    def train(self):
        corpus_path = self.build_corpus()
        
        spm.SentencePieceTrainer.train(
            input=str(corpus_path),
            model_prefix=str(
                self.output_dir / "ganjoor"
            ),
            vocab_size=14087,
            model_type="bpe",
            character_coverage=1.0
        )