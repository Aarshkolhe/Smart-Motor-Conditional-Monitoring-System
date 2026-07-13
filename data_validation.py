import json
import os
import pandas as pd
import numpy as np

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("          TASK 7: FEATURE STORE VALIDATION        ")
print("==================================================")
print("\n")

# ==========================================================
# 1. DATA INGESTION ENGINE (AUTOPILOT CONNECTIVITY ACTIVE)
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Initializing Feature Store cloud sync...")
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(CREDENTIALS_FILE)
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    docs = db.collection("feature_store_outputs").stream()
    real_json_data = [doc.to_dict() for doc in docs]
    print("Feature store cloud download successful.")
else:
    print("No live cloud keys found yet. Running specification simulation mode...")
    
    # Simulating a raw feature store extract contaminated with common engineering anomalies
    # (NaNs, Infinities, and physical boundary limit breaches)
    firestore_json_data = """
    [
        {"record_id": 101, "temperature": 38.5, "voltage": 220.4, "vibration": 1.45},
        {"record_id": 102, "temperature": null, "voltage": 219.8, "vibration": 1.52},
        {"record_id": 103, "temperature": 42.3, "voltage": 221.1, "vibration": null},
        {"record_id": 104, "temperature": 35.0, "voltage": 1400.0, "vibration": 1.40},
        {"record_id": 105, "temperature": -99.0, "voltage": 218.5, "vibration": 3.45},
        {"record_id": 106, "temperature": 45.1, "voltage": 220.0, "vibration": "Infinity"}
    ]
    """
    # Parse data and ensure true numpy infinite types are correctly mapped
    raw_data = json.loads(firestore_json_data)
    for record in raw_data:
        if record["vibration"] == "Infinity":
            record["vibration"] = np.inf
    real_json_data = raw_data

# Load data matrix
df = pd.DataFrame(real_json_data)
print(f"Loaded {len(df)} feature store rows for verification.")
print("-" * 40 + "\n")

# ==========================================================
# 2. DEFINE PHYSICAL OPERATIONAL BOUNDARIES
# ==========================================================
# Expected engineering constraints based on the motor's equipment specs
LIMITS = {
    'temperature': {'min': 0.0, 'max': 120.0},     # Degrees Celsius
    'voltage': {'min': 150.0, 'max': 280.0},       # Volts AC
    'vibration': {'min': 0.0, 'max': 15.0}         # mm/s Amplitude
}

columns_to_check = ['temperature', 'voltage', 'vibration']

# ==========================================================
# 3. RUN AUDITS: NULLS, INFINITIES, AND RANGE BREACHES
# ==========================================================
print("--- RUNNING INDUSTRIAL DATA QUALITY AUDIT ---")
anomalies_detected = []

for idx, row in df.iterrows():
    rec_id = row['record_id']
    
    for col in columns_to_check:
        val = row[col]
        
        # Check A: Missing Values (NaN/Null)
        if pd.isna(val):
            print(f"CRITICAL: Record {rec_id} -> Column '{col}' is missing (NaN/Null)")
            anomalies_detected.append({"record_id": rec_id, "field": col, "error_type": "NaN/Null", "value": val})
            continue
            
        # Check B: Mathematical Infinity Errors
        if np.isinf(val):
            print(f"CRITICAL: Record {rec_id} -> Column '{col}' has an Infinity error")
            anomalies_detected.append({"record_id": rec_id, "field": col, "error_type": "Infinity", "value": val})
            continue
            
        # Check C: Range Boundaries Anomalies
        if val < LIMITS[col]['min'] or val > LIMITS[col]['max']:
            print(f"WARNING: Record {rec_id} -> Column '{col}' value out of limits: {val} (Expected {LIMITS[col]['min']} to {LIMITS[col]['max']})")
            anomalies_detected.append({"record_id": rec_id, "field": col, "error_type": "Range Anomaly", "value": val})

print("-" * 40 + "\n")

# ==========================================================
# 4. EXPORT COMPLIANCE DATA LOGS
# ==========================================================
# Build a structured report summary matrix for your senior
if anomalies_detected:
    df_errors = pd.DataFrame(anomalies_detected)
    print(f"Audit completed: Total anomalies flagged: {len(df_errors)}")
else:
    df_errors = pd.DataFrame(columns=["record_id", "field", "error_type", "value"])
    print("Audit completed: 100% data compliance. No anomalies detected.")

# Enforce automated target folder pathing natively
script_directory = os.path.dirname(os.path.abspath(__file__))
report_path = os.path.join(script_directory, 'feature_store_validation_report.csv')

df_errors.to_csv(report_path, index=False)
print(f"Validation compliance matrix saved cleanly to: '{report_path}'")
print("==================================================")
