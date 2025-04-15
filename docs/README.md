### Environment Setup
- Conda environment: `agentictrader` (Python 3.10).
- Install: `conda create -n agentictrader python=3.10; conda activate agentictrader; pip install -r requirements.txt`.

### DSPy Integration
- Located in `backend/llm/dspy_config.py` and `backend/agents/scout/models/dspy/`.
- Enhances ICT setup detection.

### Data Clients
- `backend/data_clients/` handles MT5, Notion, and external data.
