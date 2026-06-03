import json
from pathlib import Path

import sentencepiece as spm


class DatasetTokenizer:

    def __init__(
        self,
        model_path="tokenizer/vocab/ganjoor.model",
        dataset_path="data/datasets/mixed.jsonl",
        output_path="data/datasets/tokens.jsonl"
    ):
        self.model_path = model_path
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path)

    def build_text(self, doc):

        if doc["type"] == "corpus":
            return doc["text"]

        if doc["type"] == "instruction":
            return (
                f"### Instruction\n"
                f"{doc['instruction']}\n\n"
                f"### Input\n"
                f"{doc['input']}\n\n"
                f"### Response\n"
                f"{doc['output']}"
            )

        return ""

    def run(self):

        sp = spm.SentencePieceProcessor(
            model_file=self.model_path
        )

        with open(
            self.dataset_path,
            "r",
            encoding="utf-8"
        ) as source, open(
            self.output_path,
            "w",
            encoding="utf-8"
        ) as target:

            for line in source:

                doc = json.loads(line)

                text = self.build_text(doc)

                token_ids = sp.encode(
                    text,
                    out_type=int
                )

                target.write(
                    json.dumps(
                        token_ids,
                        ensure_ascii=False
                    )
                    + "\n"
                )

        print("Tokenization completed")