<!--
  Generated template: update the TODO sections after scanning the repo.
  This file is meant to guide AI coding agents to be productive quickly.
-->

# Copilot Instructions for AI Coding Agents

Purpose: Help AI agents understand this repository's structure, developer workflows, conventions, and important integration points so they can make focused, correct changes.

**Quick discovery (run first)**
- Run a short scan to confirm files and manifests (PowerShell):

```powershell
Get-ChildItem -File -Recurse -Depth 2 | Select-Object FullName
if (Test-Path requirements.txt) { Get-Content requirements.txt }
if (Test-Path .\data\india_housing_prices.csv) { Write-Output 'Dataset found: data\india_housing_prices.csv' }
ls .github\workflows -ErrorAction SilentlyContinue
```

**This project — Big picture**
- Title: Real Estate Investment Advisor — predicts 5-year property price and classifies "Good Investment".
- Major components (recommended layout):
  - `data/` : raw and processed CSVs (e.g., `india_housing_prices.csv`, `cleaned.csv`).
  - `notebooks/` : exploratory notebooks for EDA and visualization.
  - `src/` : scripts and modules (`src/eda.py`, `src/features.py`, `src/train.py`, `src/predict.py`).
  - `app/` : Streamlit app (`app/streamlit_app.py`).
  - `mlruns/` or `mlflow/` : MLflow tracking artifacts and registry.

**Key project-specific workflows & commands**
- Create virtual env and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```
- Run EDA scripts / notebooks:

```powershell
python src/eda.py --input data/india_housing_prices.csv --out reports/eda.html
# or open notebooks in `notebooks/`
```
- Train (example using MLflow tracking):

```powershell
mlflow run . -P data_path=data/india_housing_prices.csv -P experiment.name=realestate_training
# Or run script directly:
python src/train.py --data data/india_housing_prices.csv --output models/
```
- Launch MLflow UI:

```powershell
mlflow ui --backend-store-uri ./mlruns --port 5000
```
- Run Streamlit app:

```powershell
streamlit run app/streamlit_app.py
```

**Project-specific conventions & patterns**
- Dataset: `data/india_housing_prices.csv` — canonical input. Keep a processed `data/cleaned.csv` after preprocessing.
- Targets:
  - Regression target: `Future_Price_5Y` (predict price 5 years ahead).
  - Classification target: `Good_Investment` (binary label derived from appreciation thresholds and multi-factor score).
- Feature engineering: compute `price_per_sqft`, `age`, `amenities_count`, `school_density_score` in `src/features.py`.
- Model files: save trained models to `models/` and register top models with MLflow Model Registry.
- Experiment tracking: log params, metrics, artifacts (feature importance plots) to MLflow every run.

**Integration points & external services**
- MLflow (local or remote tracking server). Recommended local store: `./mlruns`.
- Optional: Postgres/Cloud blob for model artifacts — configure via env vars like `MLFLOW_TRACKING_URI`, `ARTIFACT_ROOT`.
- Streamlit for UI and deployment (Streamlit Cloud or containerize for production).

**When changing code — checklist for PRs produced by an AI agent**
- Add or update tests (use `pytest`) for any new preprocessing or model logic.
- Run `python -m pip install -r requirements.txt` and ensure `src/train.py` runs end-to-end on a small sample.
- Log experiments to MLflow and attach the run id in PR description.
- Update `README.md` with any new CLI args or environment variables.

**Merging guidance**
- Keep commits small and focused: `feat: add feature engineering for price_per_sqft`.
- Include expected model metric improvements and MLflow run id in PR summary.

---
Repository currently has minimal files. I can now run the discovery scan and auto-fill the `data/`, `src/`, and `app/` sections with concrete file examples — should I proceed?
