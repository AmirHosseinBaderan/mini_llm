from dataclasses import dataclass

@dataclass
class DatasetDocument:
    source: str

    poet: str

    category: str

    title: str

    text: str