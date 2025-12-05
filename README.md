# Real Estate Investment Advisor

This scaffold provides a Streamlit app to evaluate whether a property is a "Good Investment" and estimate its price after 5 years using simple heuristics and (optionally) trained ML models.

Run locally (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Files in this repo (key ones):
- `data/india_housing_prices.csv` - small sample dataset (replace with full dataset for realistic training)
- `src/utils.py` - helper utilities (price per sqft, simple heuristics)
- `src/prepare.py` - preprocessing and synthetic target creation
- `src/train.py` - training pipeline (RandomForest classifier & regressor), MLflow logging, saves models to `models/`
- `app/streamlit_app.py` - Streamlit UI that loads models (if present) and falls back to heuristics
- `.github/copilot-instructions.md` - guidance template for AI coding agents
- `requirements.txt`, `README.md` - install & run instructions

---
**Share / Link for faculty**

Repository (please share this link with faculty):

https://github.com/syr230/real-estate-prediction.git

You can mention in your submission: "Repository contains Streamlit UI, preprocessing, training scripts with MLflow logging, and sample data. Follow the README to run locally or deploy." 

**How to deploy / share the app**

Option A — Streamlit Cloud (recommended for quick sharing)
- Push your repo to GitHub (example branch `feature/streamlit-mlflow`).
- On Streamlit Cloud, connect the GitHub repo and select `app/streamlit_app.py` as the entrypoint. Streamlit Cloud will install dependencies from `requirements.txt` and launch the app.

Option B — Local deployment (demo + MLflow)
- Create and activate the venv and install deps:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
- Prepare data and train models (optional):

```powershell
python src/prepare.py
python src/train.py
```
- Launch MLflow UI (to inspect runs):

```powershell
mlflow ui --backend-store-uri ./mlruns --port 5000
```
- Run Streamlit locally and open http://localhost:8501:

```powershell
streamlit run app/streamlit_app.py
```

Option C — Docker (containerized)
- Create a `Dockerfile` that installs Python, copies the repo, installs `requirements.txt`, and runs `streamlit run app/streamlit_app.py`.
- Build and run the container with Docker or deploy to any container platform.

**Notes & troubleshooting**
- Replace the sample CSV in `data/` with the full `india_housing_prices.csv` for meaningful models.
- MLflow stores runs under `./mlruns` by default; to use a remote tracking server set `MLFLOW_TRACKING_URI`.
- If Streamlit cannot import `src.*`, the app prepends the project root to `sys.path` in `app/streamlit_app.py` — ensure you launch Streamlit from the repo root or allow the app to handle path adjustments.

---
If you'd like, I can push these README updates and the current branch to your GitHub repository now. Confirm and I will run the git commands to add the remote, push the current branch (`feature/streamlit-mlflow`) and create the remote branch.

