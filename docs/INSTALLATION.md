# Installation Guide

## Prerequisites

- Python 3.10 or 3.11
- 16 GB RAM minimum (32 GB recommended for IndoBERT fine-tuning)
- NVIDIA GPU with ≥ 8 GB VRAM (for LLM inference)
- CUDA 11.8+ or 12.x
- Optional: Neo4j 5.x, Apache Jena Fuseki, Protégé 5.6+

## Setup

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/ArsipKG.git
cd ArsipKG

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r code/requirements.txt
```

## Hugging Face Access

The LLaMA models require Hugging Face authentication:

```bash
huggingface-cli login
# Enter your HF token when prompted
```

Request access to `meta-llama/Llama-3.1-8B-Instruct` and `meta-llama/Llama-3.2-3B-Instruct` on Hugging Face Hub.

## Verifying Installation

```bash
# Quick test (no GPU needed)
python code/baselines/rule_based.py --data data/arsipdataset/splits/test.csv

# GPU test (requires CUDA + HF access)
python -c "from transformers import AutoModelForCausalLM; print('OK')"
```

## Troubleshooting

| Issue | Fix |
|---|---|
| `bitsandbytes` not loading | Reinstall: `pip install bitsandbytes --force-reinstall` |
| CUDA out of memory | Reduce batch size; check GPU usage with `nvidia-smi` |
| LLaMA gated access | Request via HF; wait for approval (usually < 24 h) |
| Neo4j connection | Check `bolt://localhost:7687` is accessible |
