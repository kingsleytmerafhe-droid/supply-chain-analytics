# Supply Chain Analytics Dashboard

A end-to-end data analytics and machine learning project built to analyse supply chain performance, identify delivery delays, and predict shipment outcomes using a Random Forest model.

Built by **Kingsley Merafhe** — Business Intelligence & Data Analytics

---

## What This Project Does

- Analyses 100 SKUs across 5 cities in India
- Identifies delay patterns, defect hotspots, and cost inefficiencies
- Predicts whether a shipment will be delayed using a trained ML model
- Visualises everything in an interactive Streamlit dashboard

---

## Project Structure

```
supply-chain-analytics/
├── dashboard.py                  # Streamlit dashboard
├── Logistics_Analytics_Kingsley.ipynb  # Full analysis notebook
├── supply_chain_data.csv         # Dataset
├── models/
│   ├── rf_model.pkl              # Trained Random Forest model
│   ├── label_encoders.pkl        # Category encoders
│   └── feature_cols.pkl          # Feature list
└── README.md
```

---

## How To Run It

### Option 1 — Google Colab (Easiest, no setup needed)

**Step 1** — Open a new Colab notebook at colab.research.google.com

**Step 2** — Run this cell to install dependencies
```python
!pip install streamlit pyngrok plotly --quiet
```

**Step 3** — Upload all project files
```python
from google.colab import files
files.upload()
# Upload: dashboard.py, supply_chain_data.csv,
#         rf_model.pkl, label_encoders.pkl, feature_cols.pkl
```

**Step 4** — Move model files into the models folder
```python
import shutil, os
os.makedirs("models", exist_ok=True)
shutil.copy("rf_model.pkl",        "models/rf_model.pkl")
shutil.copy("label_encoders.pkl",  "models/label_encoders.pkl")
shutil.copy("feature_cols.pkl",    "models/feature_cols.pkl")
print("✅ Done")
```

**Step 5** — Launch the dashboard
```python
from pyngrok import ngrok
import subprocess, time

ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # get free token at ngrok.com

process = subprocess.Popen([
    "streamlit", "run", "dashboard.py",
    "--server.port", "8501",
    "--server.headless", "true"
])
time.sleep(8)
print("✅ Live at:", ngrok.connect(8501))
```

Click the link that appears — your dashboard is live.

---

### Option 2 — Run Locally

**Requirements:** Python 3.9+

**Step 1** — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/supply-chain-analytics.git
cd supply-chain-analytics
```

**Step 2** — Install dependencies
```bash
pip install streamlit plotly pandas numpy scikit-learn xgboost joblib
```

**Step 3** — Run the dashboard
```bash
streamlit run dashboard.py
```

Open your browser at `http://localhost:8501`

---

## Dashboard Features

| Tab | What It Shows |
|-----|--------------|
| Overview | Revenue, profit margins, inspection results |
| Shipping & Logistics | Delay rates, shipping costs, carrier performance |
| Suppliers & Production | Defect hotspots, stock levels, manufacturing costs |
| ML Risk Predictor | Real model predictions with delay probability % |

---

## Tech Stack

- **Python** — Pandas, NumPy, Scikit-learn
- **Machine Learning** — Random Forest Classifier
- **Visualisation** — Plotly, Streamlit
- **Notebook** — Jupyter / Google Colab

---

## Key Findings

- 47% of shipments exceed the median shipping time
- Chennai has the highest defect rate across all locations
- Skincare generates the most revenue
- Route A is the most cost-efficient
- Road transport has the highest defect rate

---

## Future Improvements

- Connect to a live database for real-time data
- Add time series forecasting for demand planning
- Deploy permanently on Streamlit Cloud
- Add email alerts for high-risk shipments
