# Pull Request: Add Streamlit UI, data scaffold, preprocessing and training

## Summary
This PR introduces a minimal end-to-end scaffold for the "Real Estate Investment Advisor" project:
- Streamlit UI (`app/streamlit_app.py`) with model-loading and heuristic fallback
- Sample dataset (`data/india_housing_prices.csv`) and data prep script (`src/prepare.py`)
- Training script (`src/train.py`) that logs runs to MLflow and saves models to `models/`
- Utility helpers (`src/utils.py`), `requirements.txt`, and project README updates
- `.github/copilot-instructions.md` with guidance for AI coding agents

## Files changed (high level)
- `app/streamlit_app.py`
- `src/prepare.py`, `src/train.py`, `src/utils.py`
- `requirements.txt`, `README.md`, `.github/copilot-instructions.md`

## How to test
1. Create and activate venv, install deps: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt`
2. (Optional) Prepare data and train models: `python src/prepare.py` then `python src/train.py`
3. Run Streamlit: `streamlit run app/streamlit_app.py` and open `http://localhost:8501`

## Checklist
- [ ] Replace sample CSV with full dataset for realistic training
- [ ] Add unit tests for preprocessing and model inference
- [ ] Add CI job to run tests and linting
- [ ] Remove MLflow artifacts from git history (optional)

## Notes
I added a `.gitignore` to avoid committing large/auto-generated artifacts (virtual env, `mlruns/`, and `models/`). If you prefer to keep `mlruns/` in the repo for submission, let me know and I will revert the `.gitignore` entry.
