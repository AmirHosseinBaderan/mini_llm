import os
import time
import numpy as np
import torch

from training.model import MiniGPT


def get_batch(
    data,
    block_size: int,
    batch_size: int,
    device
):
    ix = torch.randint(
        len(data) - block_size - 1,
        (batch_size,)
    )

    x = torch.stack([
        torch.from_numpy(
            data[i:i + block_size]
            .astype(np.int64)
        )
        for i in ix
    ])

    y = torch.stack([
        torch.from_numpy(
            data[i + 1:i + block_size + 1]
            .astype(np.int64)
        )
        for i in ix
    ])

    x = x.to(
        device,
        non_blocking=True
    )

    y = y.to(
        device,
        non_blocking=True
    )

    return x, y


@torch.no_grad()
def evaluate(
    model,
    data,
    block_size,
    batch_size,
    device,
    loss_fn,
    eval_steps=100
):
    model.eval()

    losses = []

    for _ in range(eval_steps):

        x, y = get_batch(
            data,
            block_size,
            batch_size,
            device
        )

        logits = model(x)

        loss = loss_fn(
            logits.reshape(
                -1,
                logits.size(-1)
            ),
            y.reshape(-1)
        )

        losses.append(
            loss.item()
        )

    model.train()

    return sum(losses) / len(losses)


def train():

    # Config
    VOCAB_SIZE = 16000
    BLOCK_SIZE = 128

    BATCH_SIZE = 32

    EPOCHS = 5

    LEARNING_RATE = 3e-4

    STEPS_PER_EPOCH = 1000

    # Device
    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(
        f"Using device: {device}"
    )

    if device.type == "cuda":
        print(
            f"GPU: {torch.cuda.get_device_name(0)}"
        )
        
    # Load binary datasets
    train_data = np.memmap(
        "training/train.bin",
        dtype=np.uint16,
        mode="r"
    )

    val_data = np.memmap(
        "training/val.bin",
        dtype=np.uint16,
        mode="r"
    )

    print(
        f"Train tokens: {len(train_data):,}"
    )

    print(
        f"Val tokens: {len(val_data):,}"
    )

    # Model
    model = MiniGPT(
        vocab_size=VOCAB_SIZE,
        block_size=BLOCK_SIZE
    )

    model.to(device)

    total_params = sum(
        p.numel()
        for p in model.parameters()
    )

    print(
        f"Parameters: {total_params:,}"
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE
    )

    loss_fn = torch.nn.CrossEntropyLoss()

    use_amp = (
        device.type == "cuda"
    )

    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=use_amp
    )

    # Training
    for epoch in range(EPOCHS):

        model.train()

        epoch_loss = 0.0

        start_time = time.time()

        print(
            f"\n===== Epoch {epoch + 1}/{EPOCHS} ====="
        )

        for step in range(
            STEPS_PER_EPOCH
        ):

            x, y = get_batch(
                train_data,
                BLOCK_SIZE,
                BATCH_SIZE,
                device
            )

            optimizer.zero_grad(
                set_to_none=True
            )

            with torch.amp.autocast(
                device_type=device.type,
                enabled=use_amp
            ):

                logits = model(x)

                loss = loss_fn(
                    logits.reshape(
                        -1,
                        logits.size(-1)
                    ),
                    y.reshape(-1)
                )

            scaler.scale(
                loss
            ).backward()

            scaler.step(
                optimizer
            )

            scaler.update()

            epoch_loss += (
                loss.item()
            )

            if step % 50 == 0:
                print(
                    f"epoch={epoch + 1} "
                    f"step={step} "
                    f"loss={loss.item():.4f}"
                )

        avg_train_loss = (
            epoch_loss
            / STEPS_PER_EPOCH
        )

        val_loss = evaluate(
            model,
            val_data,
            BLOCK_SIZE,
            BATCH_SIZE,
            device,
            loss_fn
        )

        duration = (
            time.time()
            - start_time
        )

        print(
            f"epoch={epoch + 1} "
            f"train_loss={avg_train_loss:.4f} "
            f"val_loss={val_loss:.4f} "
            f"time={duration:.1f}s"
        )

        checkpoint = {
            "epoch": epoch + 1,
            "model_state_dict":
                model.state_dict(),
            "optimizer_state_dict":
                optimizer.state_dict(),
            "train_loss":
                avg_train_loss,
            "val_loss":
                val_loss,
        }

        checkpoint_path = (
            f"training/checkpoint_epoch_{epoch + 1}.pt"
        )

        torch.save(
            checkpoint,
            checkpoint_path
        )

        print(
            f"Checkpoint saved: "
            f"{checkpoint_path}"
        )

    # Final save
    torch.save(
        model.state_dict(),
        "training/model.pt"
    )

    print(
        "\nTraining completed ✔"
    )

    print(
        "Model saved: "
        "training/model.pt"
    )