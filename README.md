# IoTanic Image Classification API

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Docker (optional)
- Intel AVX2 compatible CPU (for TensorFlow)

### Direct Run
1. Install dependencies
    ```zsh
    pip install -r requirements.txt
    ```
2. Copy .env.example to .env
    ```zsh
    cp .env.example .env
    ```
3. Start FastAPI process
    ```zsh
    python ./app/main.py
    ```
   Or you can use uvicorn
    ```zsh
    uvicorn app.main:app --port 8000 --reload
    ```
   > Use `--reload` flag to enable auto-reload on code changes

4. Open local API docs [http://localhost:8000/docs](http://localhost:7000/docs)

### Using Docker
1. Build Docker image
    ```zsh
    docker compose build
    ```
2. Run Docker container
    ```zsh
    docker compose up -d
    ```
   > Use `-d` flag to run in detached mode