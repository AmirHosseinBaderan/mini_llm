from dataclasses import dataclass

@dataclass
class Document:
    source:str
    extral_id:str
    title:str
    text:str
    url:str