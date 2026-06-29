import json
import os
import matplotlib
# Use a background rendering engine to prevent terminal freezes on Windows
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("          TASK 3: UNIVARIATE EDA ENGINE           ")
print("==================================================")
print("\n")

# ==========================================================
# 1. AUTOMATED DATA INGESTION ENGINE (NO CODE SWAPPING NEEDED)
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

# Check if the team key file has actual data inside it yet
if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Initiating Firestore cloud extraction...")
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    # Prevent double-initialization errors if script is run multiple times
    if not firebase_admin._apps:
        cred = credentials.Certificate(CREDENTIALS_FILE)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    docs = db.collection("motor_telemetry").stream()
    real_json_data = [doc.to_dict() for doc in docs]
    print("Live cloud download complete.")
else:
    print("No live database keys found yet. Running simulation mode instead...")
    # Expanded specifications-accurate dataset to simulate healthy vs faulty signals
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

# Extract only continuous numeric sensor channels for univariate plotting
sensor_channels = ['temperature', 'humidity', 'current', 'voltage', 'power', 'vibration']

# ==========================================================
# 2. GENERATE DISTRIBUTION GRAPHS (HISTOGRAM + KDE + BOX PLOTS)
# ==========================================================
print("Generating univariate statistical distributions for each sensor...")

for sensor in sensor_channels:
    print(f"Creating distribution graphs for feature: '{sensor}'...")
    
    # Instantiate a clean side-by-side plot layout frame (1 row, 2 columns)
    fig, (ax_hist, ax_box) = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
    
    # Plot 1: Combined Histogram and Kernel Density Estimate (KDE) line
    sns.histplot(data=df, x=sensor, kde=True, color='teal', ax=ax_hist, bins=5)
    ax_hist.set_title(f'{sensor.capitalize()} - Histogram & KDE Plot', fontsize=12, fontweight='bold')
    ax_hist.set_xlabel('Sensor Value')
    ax_hist.set_ylabel('Frequency Count')
    ax_hist.grid(True, linestyle='--', alpha=0.5)
    
    # Plot 2: Box Plot to instantly pinpoint medians, quartiles, and outliers
    sns.boxplot(data=df, x=sensor, color='orange', ax=ax_box)
    ax_box.set_title(f'{sensor.capitalize()} - Box Plot Outlier Audit', fontsize=12, fontweight='bold')
    ax_box.set_xlabel('Sensor Value')
    ax_box.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    # ==========================================================
    # 🚀 AUTOMATED PATH ENFORCEMENT (FIXED FOR CORRECT STORAGE)
    # ==========================================================
    # Find exactly where this script file lives on your disk right now
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    filename = f'distribution_{sensor}.png'
    
    # Combine the folder path and the filename into a forced destination
    full_save_path = os.path.join(script_directory, filename)
    
    # Save the chart directly into the repository folder workspace
    plt.savefig(full_save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
print("\nSuccess! Generated 6 independent distribution visual profiles.")
print("==================================================")
