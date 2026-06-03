import torch
import torch.nn as nn


class MiniGPT(nn.Module):

    def __init__(
        self,
        vocab_size: int,
        block_size: int = 128,
        embed_dim: int = 256,
        num_heads: int = 4,
        num_layers: int = 4,
        dropout: float = 0.1
    ):
        super().__init__()

        self.block_size = block_size

        self.token_embedding = nn.Embedding(
            vocab_size,
            embed_dim
        )

        self.position_embedding = nn.Embedding(
            block_size,
            embed_dim
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dropout=dropout,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.ln = nn.LayerNorm(embed_dim)

        self.head = nn.Linear(
            embed_dim,
            vocab_size
        )

    def forward(self, x):

        batch_size, seq_len = x.shape

        positions = torch.arange(
            seq_len,
            device=x.device
        )

        positions = positions.unsqueeze(0)

        token_emb = self.token_embedding(x)

        pos_emb = self.position_embedding(positions)

        x = token_emb + pos_emb

        mask = torch.triu(
            torch.ones(seq_len, seq_len, device=x.device),
            diagonal=1
        ).bool()

        x = self.transformer(
            x,
            mask=mask
        )

        x = self.ln(x)

        logits = self.head(x)

        return logits