# HexaSLM

HexaSLM is a project designed for fine-tuning and inference of Large Language Models (LLMs) using [Unsloth](https://github.com/unslothai/unsloth), capable of making LLM training 2x faster and using 70% less memory.

## Project Structure

```
HexaSLM/
├── data/               # Data storage
│   ├── raw/            # Original, immutable data
│   └── processed/      # Cleaned and prepared data
├── models/             # Model checkpoints and adapters (ignored by git)
├── notebooks/          # Jupyter notebooks for experimentation
├── src/                # Source code
│   └── hexa_slm/       # Main package
│       ├── data/       # Data processing scripts
│       ├── models/     # Training and inference scripts
│       └── utils/      # Utility functions
├── outputs/            # Training logs and results (ignored by git)
├── configs/            # Configuration files
├── pyproject.toml      # Project configuration and dependencies
└── README.md           # Project documentation
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd HexaSLM
    ```

2.  **Install dependencies:**
    This project uses `pyproject.toml` for dependency management. You can use `pip` or preferably `uv`.

    ```bash
    # Using pip
    pip install .

    # Using uv (recommended)
    uv sync
    ```

    *Note: Unsloth is installed directly from GitHub to ensure the latest version.*

## Usage

### Fine-tuning
(Add instructions for fine-tuning scripts once implemented)

### Inference
(Add instructions for inference scripts once implemented)

## License
MIT
