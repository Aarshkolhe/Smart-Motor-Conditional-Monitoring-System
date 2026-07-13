import json
import os
import matplotlib
# Force background rendering engine to completely eliminate terminal pop-up freezes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("          TASK 5: CORRELATION ENGINE              ")
print("==================================================")
print("\n")

# ==========================================================
# 1. DATA INGESTION ENGINE (AUTOPILOT CONNECTIVITY ACTIVE)
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

# Automated switch logic - checks if real cloud database keys are deployed yet
if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Initializing Firestore cloud data stream...")
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(CREDENTIALS_FILE)
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    docs = db.collection("motor_telemetry").stream()
    real_json_data = [doc.to_dict() for doc in docs]
    print("Live database stream extraction successful.")
else:
    print("No live cloud keys found yet. Running specification simulation mode...")
    # Expanded specifications-accurate dataset to calculate correlations
    firestore_json_data = """
    [
        {"temperature": 35.2, "humidity": 60, "current": 12.1, "voltage": 220.4, "power": 2.61, "vibration": 1.45},
        {"temperature": 36.1, "humidity": 59, "current": 11.9, "voltage": 219.8, "power": 2.58, "vibration": 1.52},
        {"temperature": 38.5, "humidity": 61, "current": 14.2, "voltage": 221.1, "power": 2.85, "vibration": 2.10},
        {"temperature": 35.0, "humidity": 60, "current": 12.0, "voltage": 220.0, "power": 2.60, "vibration": 1.40},
        {"temperature": 42.3, "humidity": 62, "current": 16.5, "voltage": 218.5, "power": 3.10, "vibration": 3.45},
        {"temperature": 34.8, "humidity": 60, "current": 11.8, "voltage": 220.1, "power": 2.55, "vibration": 1.38},
        {"temperature": 36.5, "humidity": 58, "current": 12.4, "voltage": 219.5, "power": 2.64, "vibration": 1.60},
        {"temperature": 55.2, "humidity": 65, "current": 19.8, "voltage": 217.2, "power": 4.10, "vibration": 5.80},
        {"temperature": 58.1, "humidity": 66, "current": 21.2, "voltage": 216.8, "power": 4.35, "vibration": 6.22},
        {"temperature": 62.4, "humidity": 68, "current": 23.5, "voltage": 215.1, "power": 4.90, "vibration": 7.45}
    ]
    """
    real_json_data = json.loads(firestore_json_data)

# Unpack dataset matrix
df = pd.DataFrame(real_json_data)

# Isolate numeric columns for mathematical correlation plotting
numeric_df = df[['temperature', 'humidity', 'current', 'voltage', 'power', 'vibration']]

# ==========================================================
# 2. COMPUTE CORRELATION MATRIX (PEARSON COEFFICIENTS)
# ==========================================================
print("\n--- CALCULATING SENSOR CORRELATION MATRIX ---")
correlation_matrix = numeric_df.corr()
print(correlation_matrix.round(2))
print("-" * 40)

# ==========================================================
# 3. IDENTIFY REDUNDANT FEATURES (THRESHOLD > 0.90)
# ==========================================================
print("\nScanning for redundant or highly correlated features (Threshold > 0.90)...")
redundant_found = False

for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        score = correlation_matrix.iloc[i, j]
        if abs(score) > 0.90:
            col1 = correlation_matrix.columns[i]
            col2 = correlation_matrix.columns[j]
            # Emoji completely removed from this print statement below:
            print(f"ALERT: High redundancy detected between '{col1}' and '{col2}' (Score: {score:.2f})")
            redundant_found = True

if not redundant_found:
    print("Clear! No redundant features crossing the 0.90 threshold value.")

# ==========================================================
# 4. GENERATE CORRELATION HEATMAP VISUALIZATION
# ==========================================================
print("\nRendering statistical correlation heatmap...")
plt.figure(figsize=(10, 8))

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)

plt.title('Motor Telemetry Profile: Sensor Feature Correlation Heatmap', fontsize=13, fontweight='bold')
plt.tight_layout()

# Force save destination straight to your active project folder path on autopilot
script_dir = os.path.dirname(os.path.abspath(__file__))
image_save_path = os.path.join(script_dir, 'sensor_correlation_heatmap.png')

plt.savefig(image_save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Success! Heatmap visualization exported natively to: '{image_save_path}'")
print("==================================================")
