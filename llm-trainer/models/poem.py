from dataclasses import dataclass

@dataclass
class Poem:
    id:int
    title:str
    full_url:str
    
@dataclass
class RawPoem:
    poem_id: int
    data: dict