import json
from typing import Dict, List, Any


class DatasetBuilder:
    def __init__(self):
        pass

    def build_corpus(self, poem: Dict[str, Any]) -> Dict:
        return {
            "type": "corpus",
            "text": poem["text"]
        }

    def build_summary(self, poem: Dict[str, Any]) -> Dict:
        return {
            "type": "instruction",
            "instruction": "این شعر را خلاصه کن",
            "input": poem["text"],
            "output": ""  # بعداً با rule-based یا LLM پر میشه
        }

    def build_analysis(self, poem: Dict[str, Any]) -> Dict:
        return {
            "type": "instruction",
            "instruction": "این شعر را تحلیل ادبی کن",
            "input": poem["text"],
            "output": ""
        }

    def build_qa(self, poem: Dict[str, Any]) -> List[Dict]:
        return [
            {
                "type": "instruction",
                "instruction": "موضوع این شعر چیست؟",
                "input": poem["text"],
                "output": ""
            }
        ]

    def build_all(self, poem: Dict[str, Any]) -> List[Dict]:
        """
        خروجی نهایی چندتایی برای هر شعر
        """

        samples = []

        samples.append(self.build_corpus(poem))
        samples.append(self.build_summary(poem))
        samples.append(self.build_analysis(poem))
        samples.extend(self.build_qa(poem))

        return samples