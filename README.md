# Smart Motor Condition Monitoring System

## Task 1 & 2: Data Analytics & Support Setup

This repository contains the data profiling pipeline for parsing incoming motor telemetry data. The pipeline supports both offline simulation testing and a hot-swap transition to live cloud infrastructure.

---

## How the Code Architecture Works
The script data_inspection.py is split into two sections:
1. **Section 1 (Database Switch Logic):** Detects if keys are present. If missing or empty, it automatically triggers a local JSON simulation.
2. **Section 2 (Analytics Pipeline):** Loads data into a Pandas DataFrame, verifies shapes/types, and exports automated summary statistics.

---

## How to Swap to Live Firestore Data (When Keys Arrive)

1. Drop your credentials file into this directory and name it **firebase-credentials.json**.
2. Install the Google Cloud dependency in your terminal:
   ```bash
   pip install firebase-admin
   ```
3. Open **data_inspection.py** and replace its entire content with this live production code:

```python
import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("    TASK 1: LIVE JSON TELEMETRY DATA INSPECTION   ")
print("==================================================")
print("\n")

# ==========================================================
# SECTION 1: LIVE FIRESTORE DATABASE CONNECTIVITY
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

print("Connecting to live Firestore database using keys...")

if not os.path.exists(CREDENTIALS_FILE) or os.path.getsize(CREDENTIALS_FILE) <= 2:
    print(f"ERROR: Missing credentials key data inside '{CREDENTIALS_FILE}'!")
    exit()

cred = credentials.Certificate(CREDENTIALS_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("motor_telemetry").stream()
real_json_data = [doc.to_dict() for doc in docs]

print("Live connection successful! Data downloaded.")
print("-" * 40 + "\n")

# ==========================================================
# SECTION 2: DATAFRAME ANALYTICS PIPELINE
# ==========================================================
df = pd.DataFrame(real_json_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

print("--- [1/4] DATASET SHAPE ---")
print(f"Total Database Records (Rows): {df.shape[0]}")
print(f"Total Telemetry Fields (Columns): {df.shape[1]}")
print("\n" + "-"*40 + "\n")

print("--- [2/4] SENSOR DATA TYPES ---")
print(df.dtypes)
print("\n" + "-"*40 + "\n")

print("--- [3/4] SAMPLE VALUES (Telemetry Matrix) ---")
print(df)
print("\n" + "-"*40 + "\n")

print("--- [4/4] GENERATING SUMMARY STATISTICS ---")
summary_stats = df.describe().T
print(summary_stats[['count', 'mean', 'std', 'min', 'max']])
print("\n" + "-"*40 + "\n")

summary_stats.to_csv('live_telemetry_summary_statistics.csv')
print("Done! Analysis exported successfully to 'live_telemetry_summary_statistics.csv'")
print("==================================================")
```

---

## 📊 Task 3: Univariate Exploratory Data Analysis (EDA)

The file `univariate_eda.py` automatically scans every independent hardware telemetry channel and profiles its underlying statistical structure. It generates split-screen visual charts to evaluate operational distributions and catch outliers.

### Dependencies Setup
To activate the advanced charting engine, make sure the statistical visualization package is installed:
```bash
pip install seaborn matplotlib pandas
```

### Feature Output Metrics
When executed, this feature automatically outputs 6 separate high-resolution report images directly into the repository workspace folder:
* `distribution_temperature.png` - Thermal bounds distribution
* `distribution_humidity.png` - Ambient environmental moisture profile
* `distribution_current.png` - Amperage load distribution
* `distribution_voltage.png` - Line voltage feed stability profile
* `distribution_power.png` - Real-time kilowatt consumption spread
* `distribution_vibration.png` - Structural mechanical vibration metrics

### Visual Layout Design per Channel
* **Left Panel (Histogram + KDE Wave):** Maps value frequencies and smooth probability density paths to analyze hardware balance stability.
* **Right Panel (Box Plot):** Pinpoints operational medians, quartiles, and maps isolated anomaly spikes as explicit outlier data points.

---

## Security & Git Operations
Your workspace includes a .gitignore file that masks firebase-credentials.json. This ensures your private team database access keys remain safe on your personal computer and are never accidentally uploaded to GitHub.

### Save your current progress locally:
Run these commands in your VS Code terminal to finalize your branch ledger:

```bash
# 1. Stage all your current project files, graphs, and documentation
git add .

# 2. Permanently save the progress to your local task branch
git commit -m "feat: complete task 3 - implement automated univariate distribution pipelines"
```
