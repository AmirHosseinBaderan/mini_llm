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
crawl_all    - Download poems from Ganjoor API
process      - Process raw poem data
export       - Export dataset in JSONL format
train_tokenizer - Train SentencePiece tokenizer
tokenize     - Tokenize the dataset
build_bins   - Build training bins
train        - Train the model
generate     - Generate text from trained model
pipeline     - Run full pipeline (crawl + process + export)
```

### Data Flow

1. **Crawling** (`crawlers/ganjoor.py`): Fetches poets, categories, and poems from Ganjoor API
2. **Processing** (`processors/poem_processor.py`): Cleans and extracts verses from raw poems
3. **Dataset Building** (`dataset/builder.py`): Creates multiple sample types:
   - Corpus samples (raw poem text)
   - Summarization samples (first/last verses)
   - Analysis samples (rule-based literary analysis)
   - Q&A samples (topic and characteristics)
4. **Tokenization** (`tokenizer/`): Trains SentencePiece BPE tokenizer
5. **Training** (`training/train.py`): Trains MiniGPT transformer model
6. **Generation** (`training/generate.py`): Generates text using trained model

## Implementation Details

### Model Architecture (`training/model.py`)

- **MiniGPT**: A small GPT-style transformer with:
  - Token embedding (vocab_size=16000, embed_dim=256)
  - Position embedding (block_size=128)
  - 4-layer Transformer encoder (4 attention heads)
  - Layer normalization and linear head

### Tokenizer (`tokenizer/train_tokenizer.py`, `tokenizer/tokenize_dataset.py`)

- Uses SentencePiece BPE model
- Vocabulary size: 14,087 tokens
- Character coverage: 1.0 (supports all Persian characters)
- Processes corpus and instruction formats

### Training Configuration

- Framework: PyTorch
- Optimizer: AdamW (lr=3e-4)
- Loss: CrossEntropyLoss
- Batch size: 16
- Block size: 128
- Epochs: 5

### Directory Structure

```
llm-trainer/
├── crawlers/          # Ganjoor API crawling
├── processors/        # Poem text processing
├── dataset/           # Dataset building and export
├── tokenizer/         # SentencePiece tokenizer
├── training/          # Model and training
├── storage/           # Raw data and state storage
└── models/            # Data models
```

## Usage

```bash
# Full pipeline
python main.py pipeline

# Train model
python main.py train

# Generate text
python main.py generate
```