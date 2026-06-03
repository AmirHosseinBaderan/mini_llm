import json
import numpy as np
from pathlib import Path


class BinBuilder:

    def __init__(
        self,
        tokenized_path="data/datasets/tokens.jsonl",
        output_dir="training"
    ):
        self.tokenized_path = Path(tokenized_path)
        self.output_dir = Path(output_dir)

    def run(self):

        all_tokens = []

        with open(
            self.tokenized_path,
            "r",
            encoding="utf-8"
        ) as f:

            for line in f:

                tokens = json.loads(line)

                all_tokens.extend(tokens)

        tokens = np.array(
            all_tokens,
            dtype=np.uint16
        )

        split = int(
            len(tokens) * 0.9
        )

        train_tokens = tokens[:split]
        val_tokens = tokens[split:]

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        train_tokens.tofile(
            self.output_dir / "train.bin"
        )

        val_tokens.tofile(
            self.output_dir / "val.bin"
        )

        print("Train tokens:", len(train_tokens))
        print("Val tokens:", len(val_tokens))