import torch
from training.model import MiniGPT
import sentencepiece as spm

class Generator:
    def __init__(self,model_path,sp_model_path,vocab_size,block_size=128):
        self.device = "cpu"
        self.block_size = block_size
        self.model = MiniGPT(
            vocab_size=vocab_size,
            block_size=block_size
        )
        
        self.model.load_state_dict(
            torch.load(model_path,map_location=self.device)
        )
        
        self.model.eval()
        
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(sp_model_path)
        
    @torch.no_grad()
    def generate(self,prompt:str,max_new_tokens:int = 100,temperture:float = 1.0):
        tokens = self.sp.Encode(prompt,out_type=int)
        tokens = torch.tensor(tokens).unsqueeze(0)
        
        for _ in range(max_new_tokens):
            tokens_cond = tokens[:,self.block_size:]
            logits = self.model(tokens_cond)
            logits = logits[:,-1,:] / temperture
            
            probs = torch.softmax(logits,dim=-1)
            next_token = torch.multinomial(probs,num_samples=1)
            
            tokens = torch.cat([tokens,next_token],dim=1)
            
        return self.sp.Decode(tokens[0].tolist())