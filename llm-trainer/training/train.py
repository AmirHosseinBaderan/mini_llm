import torch

from torch.utils.data import DataLoader

from training.dataset import TokenDataset
from training.model import MiniGPT


def train():

    with open(
        "data/datasets/tokens.txt",
        encoding="utf-8"
    ) as f:

        tokens = list(
            map(
                int,
                f.read().split()
            )
        )

    VOCAB_SIZE = 16000
    BLOCK_SIZE = 128
    BATCH_SIZE = 16
    EPOCHS = 5

    dataset = TokenDataset(
        tokens,
        BLOCK_SIZE
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    device = "cpu"

    model = MiniGPT(
        vocab_size=VOCAB_SIZE,
        block_size=BLOCK_SIZE
    )

    model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=3e-4
    )

    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(EPOCHS):

        model.train()

        total_loss = 0

        for step, (x, y) in enumerate(loader):

            x = x.to(device)
            y = y.to(device)

            logits = model(x)

            loss = loss_fn(
                logits.reshape(-1, logits.size(-1)),
                y.reshape(-1)
            )

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

            if step % 100 == 0:
                print(
                    f"epoch={epoch} step={step} loss={loss.item():.4f}"
                )

        print(
            f"epoch={epoch} avg_loss={total_loss/len(loader):.4f}"
        )

    torch.save(
        model.state_dict(),
        "training/model.pt"
    )