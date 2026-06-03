import re
from typing import Dict,Any,List

class PoemProcessor:
    def __init__(self):
        pass
    
    def clean_text(self,text:str)-> str:
        # clean text
        if not text:
            return ""
        
        text = text.replace("\r","\n")
        # remove spaces
        text = re.sub(r"\n{3,}","\n\n",text)
        
        # trime lines
        lines = [line.strip() for line in text.split("\n")]
        # delete empty lines
        lines = [line for line in lines if line]
        
        return "\n".join(lines)
    
    def extract_verses(self,poem:Dict[str,Any])-> List[str]:
        verses = poem.get("verses",[])
        
        if verses:
            return [
                v.get("text","").strip()
                for v in verses
                if v.get("text")
            ]
            
        plain = poem.get("plainText","")
        return self.clean_text(plain).split("\n")
    
    def build(self,poem:Dict[str,Any]) -> Dict[str,Any]:
        # convert poem to data cleaned 
        
        poem_id = poem.get("id")
        title = poem.get("title","")
        text = self.clean_text(poem.get("plainText",""))
        
        verses = self.extract_verses(poem)
        
        return{
            "id":poem_id,
            "title":title,
            "text":text,
            "verses":verses,
            "meta":{
                "source":"ganjoor"
            }
        }