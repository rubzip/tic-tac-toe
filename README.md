# Tic-Tac-Toe Social Network

This is a Tic-Tac-Toe game that can be played with friends over the internet.

## Backend Setup

### Prerequisites
- [uv](https://github.com/astral-sh/uv) installed.

### Configuration
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

### Running the API
To start the FastAPI server:
```bash
uv run uvicorn app.main:app --reload
```

### Running Tests
To run the test suite correctly (ensuring the `app` package is in the Python path):
```bash
uv run python -m pytest
```


