# Mini LLM

A Persian poetry language model trainer built on PyTorch, designed to train a small GPT-style model on classical Persian poems from Ganjoor.

## What This Project Does

**English:**  
This project crawls, processes, and trains a small language model on Persian poetry. It fetches poems from the Ganjoor poetry database, processes them into a structured format, and trains a transformer-based GPT model to generate and understand Persian poetic text.

**فارسی:**  
این پروژه یک مدل زبانی کوچک را روی شعرهای کلاسیک فارسی آموزش می‌دهد. شعرها را از پایگاه دادهٔ گنجور می‌گیرد، پردازش می‌کند و مدل GPT مبتنی بر ترنسفورمر را برای تولید و درک متون شاعرانه فارسی آموزش می‌دهد.

## How This Project Works

### Pipeline Commands

```
Commands:
1. crawl_all      - Download poems from Ganjoor API
2. export         - Export dataset in JSONL format
3. train_tokenizer - Train SentencePiece tokenizer
4. tokenize       - Tokenize the dataset
5. build_bins     - Build training bins
6. train          - Train the model
7. generate       - Generate text from trained model
```

### Data Flow

1. **Crawling** (`crawlers/ganjoor.py`): Fetches poets, categories, and poems from Ganjoor API
2. **Processing** (`processors/poem_processor.py`): Cleans and extracts verses from raw poems (called during crawl)
3. **Dataset Building** (`dataset/builder.py`): Creates multiple sample types per poem:
   - Corpus samples (raw poem text)
   - Summarization samples (first/last verses)
   - Analysis samples (rule-based literary analysis)
   - Q&A samples (topic and characteristics)
4. **Export** (`dataset/exporter.py`): Combines all processed data into `data/datasets/mixed.jsonl`
5. **Tokenization** (`tokenizer/train_tokenizer.py`): Trains SentencePiece BPE tokenizer
6. **Tokenization** (`tokenizer/tokenize_dataset.py`): Converts text to token IDs
7. **Build Bins** (`training/build_bins.py`): Creates binary train/val files
8. **Training** (`training/train.py`): Trains MiniGPT transformer model
9. **Generation** (`training/generate.py`): Generates Persian poetry using trained model

## Environment Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Installation on Linux

#### 1. Clone or navigate to the project

```bash
cd llm-trainer
```

#### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

#### 3. Install dependencies

**For CPU only:**
```bash
pip install -r requirements.txt
```

**For GPU (NVIDIA CUDA):**
```bash
# Ensure NVIDIA drivers are installed
nvidia-smi

# Install PyTorch with CUDA support first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Then install remaining dependencies
pip install -r requirements.txt
```

#### 4. Verify installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Installation on macOS

#### 1. Clone or navigate to the project

```bash
cd llm-trainer
```

#### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

#### 3. Install dependencies

**For CPU only (Apple Silicon or Intel):**
```bash
pip install -r requirements.txt
```

**For GPU (Apple Silicon M1/M2/M3 - Metal acceleration):**
```bash
# Install PyTorch with Metal support
pip install torch torchvision torchaudio

# Then install remaining dependencies
pip install -r requirements.txt
```

**Note:** On Apple Silicon Macs, PyTorch automatically uses Metal Performance Shaders (MPS) for GPU acceleration. The training script will detect and use `mps` device when available.

#### 4. Verify installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'MPS available: {torch.backends.mps.is_available()}')"
```

### Installation on Windows

#### 1. Clone or navigate to the project

```bash
cd llm-trainer
```

#### 2. Create and activate a virtual environment

```powershell
# Using Command Prompt
python -m venv .venv
.venv\Scripts\activate

# Using PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1

# Using Git Bash
python -m venv .venv
source .venv/Scripts/activate
```

#### 3. Install dependencies

**For CPU only:**
```bash
pip install -r requirements.txt
```

**For GPU (NVIDIA CUDA):**
```bash
# Install PyTorch with CUDA support first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Then install remaining dependencies
pip install -r requirements.txt
```

**Prerequisites for GPU on Windows:**
- NVIDIA GPU with CUDA support
- NVIDIA GeForce Game Ready Driver or Studio Driver (latest version)
- CUDA Toolkit 11.8 or 12.1 (depending on PyTorch version)

#### 4. Verify installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### CPU vs GPU Configuration

The project automatically detects and uses the best available device:

| Platform | Device Priority | Notes |
|----------|----------------|-------|
| Linux with NVIDIA GPU | `cuda` | Full GPU acceleration with AMP |
| Windows with NVIDIA GPU | `cuda` | Full GPU acceleration with AMP |
| macOS Apple Silicon | `mps` | Metal Performance Shaders acceleration |
| macOS Intel | `cpu` | No GPU acceleration available |
| Any platform without GPU | `cpu` | Slower training, no AMP |

#### GPU-Specific Features

When GPU is available, the training script (`training/train.py`) automatically:
- Uses CUDA device (`torch.device("cuda")`)
- Enables Automatic Mixed Precision (AMP) via `torch.amp.autocast`
- Uses `GradScaler` for stable gradient computation
- Prints GPU name and device info

#### CPU-Only Training

Training on CPU will work but is significantly slower. To optimize CPU training:
- Reduce `BATCH_SIZE` in `training/train.py` (e.g., from 32 to 8 or 4)
- Reduce `EPOCHS` for testing (e.g., from 5 to 2)
- The project automatically disables AMP on CPU

### Quick Start Example

```bash
# 1. Install dependencies
cd llm-trainer
pip install -r requirements.txt

# 2. Crawl poems (automatically processes and saves dataset samples)
python main.py crawl_all

# 3. Export all processed data to single JSONL file
python main.py export

# 4. Train tokenizer
python main.py train_tokenizer

# 5. Tokenize dataset
python main.py tokenize

# 6. Build binary files for training
python main.py build_bins

# 7. Train the model
python main.py train

# 8. Generate Persian poetry
python main.py generate
# Enter prompt when asked
```

## Implementation Details

### Training Configuration

- **Framework**: PyTorch - Deep learning framework for tensor computation and neural networks
- **Optimizer**: AdamW (lr=3e-4) - Adam with weight decay, learning rate 0.0003 for stable convergence
- **Loss**: CrossEntropyLoss - Standard loss for language modeling (predicts next token)
- **Batch size**: 32 - Number of sequences processed in parallel during training
- **Block size**: 128 - Context window length (sequence of 128 tokens)
- **Epochs**: 5 - Number of full passes through the training data
- **Steps per epoch**: 1000 - Training iterations per epoch
- **AMP**: Automatic Mixed Precision for CUDA acceleration

### Model Architecture (`training/model.py`)

- **MiniGPT**: A small GPT-style transformer with:
  - Token embedding (vocab_size=16000, embed_dim=256)
  - Position embedding (block_size=128)
  - 4-layer Transformer encoder (4 attention heads)
  - Layer normalization and linear head

### Configuration (`training/config.py`)

- **GPTConfig**: Centralized configuration for model hyperparameters
  - `vocab_size=16000`, `block_size=128`
  - `n_layer=4`, `n_head=4`, `n_embd=256`
  - `dropout=0.1`

### Dataset (`training/dataset.py`, `training/train.py`)

- **TokenDataset** (dataset.py): Creates training sequences with input-target pairs
- **Binary Data Loading** (train.py): Uses numpy memmap for efficient large file handling
- Sliding window approach: input is tokens[t:t+block_size], target is tokens[t+1:t+block_size+1]
- Loads `training/train.bin` and `training/val.bin` for training/validation

### Generation (`training/generate.py`)

- Loads trained model (`training/model.pt`) and tokenizer
- Autoregressive decoding with temperature-controlled sampling
- Uses causal mask for autoregressive prediction

### Training Loop (`training/train.py`)

- Uses numpy memmap for memory-efficient data loading
- Saves checkpoints after each epoch (`training/checkpoint_epoch_N.pt`)
- Reports train/validation loss and training time per epoch

### Bin Builder (`training/build_bins.py`)

- Converts tokenized JSONL to binary format for efficient training
- Splits data: 90% train, 10% validation
- Saves as `train.bin` and `val.bin`

### Tokenizer (`tokenizer/train_tokenizer.py`, `tokenizer/tokenize_dataset.py`)

- Uses SentencePiece BPE model
- Vocabulary size: 14,087 tokens (trained from corpus)
- Character coverage: 1.0 (supports all Persian characters)
- Processes corpus and instruction formats into token IDs
- Default paths: `tokenizer/vocab/ganjoor.model`, `data/datasets/mixed.jsonl`

### Storage (`storage/`)

- **RawStorage**: Saves raw poem and dataset JSON files to `data/raw/`
- **StateStorage**: Tracks crawl progress (`state.json`) to resume interrupted runs
- **FileCache**: HTTP response caching with SHA256 hashing to avoid redundant API calls

### Crawling Strategy (`crawlers/ganjoor_client.py`, `crawlers/http_client.py`)

- Uses Ganjoor REST API (`https://api.ganjoor.net/api`)
- Recursive traversal: poets → categories → poems
- Rate limiting with 0.5s delay between requests
- Resume capability via state.json tracking

### Directory Structure

```
llm-trainer/
├── crawlers/          # Ganjoor API crawling
├── processors/        # Poem text processing (imported by crawlers)
├── dataset/           # Dataset building and export
├── tokenizer/         # SentencePiece tokenizer
├── training/          # Model and training
├── storage/           # Raw data and state storage
├── models/            # Data models (Poem, Category)
└── validators/        # Dataset validation
```

## Troubleshooting

### Common Issues

**CUDA out of memory:**
- Reduce `BATCH_SIZE` in `training/train.py`
- Reduce `BLOCK_SIZE` in `training/config.py`

**SentencePiece installation fails:**
- On Linux: `sudo apt-get install cmake`
- On Windows: Install Visual Studio Build Tools

**Import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Permission errors on Linux/macOS:**
- Ensure you have write permissions in the project directory
- Run `chmod -R 755 .` if needed

### Notes

- The first run (`crawl_all`) may take several hours depending on your internet connection and the amount of poetry data
- Training on CPU can take significantly longer than GPU
- The trained model files are saved in the `training/` directory
