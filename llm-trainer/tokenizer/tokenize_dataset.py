import json
import struct
from pathlib import Path

from tokenizer.tokenizer_loader import Tokenizer

class DatasetTokenizer:
    def __init__(
        self,
        dataset_path="data/datasets/mixed.jsonl"
    ):

        self.dataset_path = Path(
            dataset_path
        )

        self.output_dir = Path(
            "data/tokenized"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.tokenizer = Tokenizer()
        
    def run(self):

        bin_path = self.output_dir / "train.bin"
        idx_path = self.output_dir / "train.idx"

        offset = 0

        with open(bin_path, "wb") as bin_file:

            with open(idx_path, "wb") as idx_file:

                with open(
                    self.dataset_path,
                    "r",
                    encoding="utf-8"
                ) as dataset:

                    for line in dataset:

                        doc = json.loads(line)

                        tokens = self.tokenizer.encode(
                            doc["text"]
                        )

                        idx_file.write(
                            struct.pack(
                                "<Q",
                                offset
                            )
                        )

                        for token in tokens:

                            bin_file.write(
                                struct.pack(
                                    "<I",
                                    token
                                )
                            )

                        offset += len(tokens)