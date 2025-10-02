# MLOps Regression Demo (Draft)

This folder turns the simple Ames Housing regression notebook into a miniature “production” experience for 3rd-year students. The goal is to walk through the steps needed to move a model from experimentation to a running application.

## Learning Objectives

- Understand how to break notebook work into reusable Python modules.
- Automate model training, serialization, and loading.
- Simulate data arrival and serve predictions via a lightweight UI (Streamlit).
- Introduce configuration control, basic testing, and logging.

## Project Layout

```
course 2/
├─ A_Regression_Example.ipynb        # original exploration notebook
├─ README.md                         # this guide
├─ requirements.txt                  # runtime dependencies
├─ configs/
│  └─ default.yaml                  # training + app configuration
├─ data/
│  ├─ raw/                          # downloaded Ames sample
│  └─ processed/                    # cleaned data ready for training
├─ models/
│  └─ model.pkl                     # trained model artifact (generated)
├─ artifacts/
│  └─ feature_stats.json            # metadata for simulator (generated)
├─ logs/
│  └─ events.log                    # runtime logs (generated)
├─ src/
│  ├─ __init__.py                   # package marker
│  ├─ config.py                     # load + validate settings
│  ├─ data_prep.py                  # data ingestion & preprocessing
│  ├─ train.py                      # train + persist model
│  ├─ predict.py                    # inference helper
│  └─ simulator.py                  # new-house event generator
├─ app/
│  └─ streamlit_app.py              # interactive UI for the demo
└─ tests/
   ├─ __init__.py
   ├─ test_preprocessing.py
   └─ test_predict.py
```

Generated files (`model.pkl`, `feature_stats.json`, `events.log`) appear after running the scripts and should not be committed to git.

## Teaching Flow

1. **Revisit the notebook** to remind students of the dataset and baseline model.
2. **Explain the folder layout** and why modularization matters in MLOps.
3. **Data preparation (`src/data_prep.py`)**
   - Download a sample of the Ames dataset into `data/raw/`.
   - Clean and encode features.
   - Save processed CSV to `data/processed/`.
4. **Training (`src/train.py`)**
   - Load processed data.
   - Train a `LinearRegression` model from scikit-learn.
   - Persist weights to `models/model.pkl` and summarize feature stats to `artifacts/feature_stats.json`.
5. **Prediction (`src/predict.py`)**
   - Provide a `load_model()` helper.
   - Expose a `predict_price()` function that takes a single house payload.
6. **Data simulation (`src/simulator.py`)**
   - Generate new house events at a configurable cadence.
   - Pull feature ranges from the stats artifact to keep data realistic.
7. **Serving application (`app/streamlit_app.py`)**
   - Use Streamlit to display ongoing “new house” events.
   - Show predicted price and optional true price to discuss model error.
   - Make cadence adjustable via sidebar controls.
8. **Testing (`tests/`)**
   - Add small unit tests to ensure preprocessing removes nulls and predictions are non-negative.
   - Emphasize how tests provide confidence when refactoring.
9. **Run-through**
   - `python -m venv .venv` & activate.
   - `pip install -r requirements.txt`.
   - `python -m src.train --config configs/default.yaml`.
   - `streamlit run app/streamlit_app.py`.

## Suggested Workshop Timeline (90 min)

- **Intro & context (10 min):** Review notebook, highlight limitations.
- **Refactoring walkthrough (25 min):** Discuss each module (`data_prep`, `train`, `predict`).
- **Hands-on exercise (30 min):** Students run training script, inspect artifacts, and launch Streamlit app.
- **Monitoring & testing (15 min):** Demonstrate logs, run `pytest` on sample tests.
- **Wrap-up (10 min):** Discuss next steps (adding features, handling drift, CI/CD).

## Extensions (Optional)

- Collect latency metrics and log them for monitoring discussions.
- Add a CLI flag to simulate data drift (e.g., price spike) and observe predictions.
- Plug in a lightweight REST endpoint (FastAPI) instead of Streamlit to compare serving strategies.

Use this structure as a teaching scaffold; code placeholders below indicate where to fill in logic during workshops.


