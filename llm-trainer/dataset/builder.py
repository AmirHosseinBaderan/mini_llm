import random
from typing import Dict, List, Any


class DatasetBuilder:
    def __init__(self):
        pass

    # Core corpus (pretraining)
    def build_corpus(self, poem: Dict[str, Any]) -> Dict:
        return {
            "type": "corpus",
            "text": poem["text"]
        }

    # Summary (rule-based)
    def build_summary(self, poem: Dict[str, Any]) -> Dict:
        text = poem["text"]

        # rule-based summary = first + last couple of lines
        lines = poem["verses"]

        summary_lines = []
        if len(lines) >= 2:
            summary_lines = [lines[0], lines[-1]]
        else:
            summary_lines = lines

        summary = " / ".join(summary_lines)

        return {
            "type": "instruction",
            "instruction": "این شعر را خلاصه کن",
            "input": text,
            "output": summary
        }

    # Simple analysis (rule-based template)
    def build_analysis(self, poem: Dict[str, Any]) -> Dict:
        text = poem["text"]
        title = poem.get("title", "")

        analysis = (
            f"این شعر با عنوان «{title}» سروده شده است. "
            f"محتوای آن شامل مضامین ادبی و استعاری است و "
            f"از ساختار بیت‌محور استفاده می‌کند."
        )

        return {
            "type": "instruction",
            "instruction": "این شعر را تحلیل ادبی کن",
            "input": text,
            "output": analysis
        }

    # Q/A rule-based
    def build_qa(self, poem: Dict[str, Any]) -> List[Dict]:

        title = poem.get("title", "")
        text = poem["text"]

        qa_samples = [
            {
                "type": "instruction",
                "instruction": "موضوع این شعر چیست؟",
                "input": text,
                "output": f"موضوع شعر «{title}» است."
            },
            {
                "type": "instruction",
                "instruction": "این شعر چه ویژگی دارد؟",
                "input": text,
                "output": "این شعر دارای ساختار کلاسیک و زبان شاعرانه است."
            }
        ]

        return qa_samples

    # Final aggregator
    def build_all(self, poem: Dict[str, Any]) -> List[Dict]:

        samples = []

        samples.append(self.build_corpus(poem))
        samples.append(self.build_summary(poem))
        samples.append(self.build_analysis(poem))
        samples.extend(self.build_qa(poem))

        return samples