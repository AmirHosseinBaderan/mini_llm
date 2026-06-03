import sentencepiece as spm

class Tokenizer:
    def __init__(self,model_path="tokenizer/vocab/ganjoor.model"):
        self.processor = spm.SentencePieceProcessor(
            model_file=model_path
        )
        
    def encode(self,text:str):
        return self.processor.encode(
            text,
            out_type=int
        )
        
    def decode(self,tokens:list[int]):
        return self.processor.decode(
            tokens
        )