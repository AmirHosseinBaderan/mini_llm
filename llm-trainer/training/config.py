from dataclasses import dataclass


@dataclass
class GPTConfig:

    vocab_size: int = 16000

    block_size: int = 128

    n_layer: int = 4
    n_head: int = 4
    n_embd: int = 256

    dropout: float = 0.1