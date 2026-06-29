import json
import os
import pandas as pd

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("    TASK 1: LIVE JSON TELEMETRY DATA INSPECTION   ")
print("==================================================")
print("\n")

# ==========================================================
# SECTION 1: DATABASE CONFIGURATION & SWITCH LOGIC
# ==========================================================
# This is the exact section you will replace when you get the real cloud keys!
CREDENTIALS_FILE = "firebase-credentials.json"

# Check if the team key file has actual data inside it yet
if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Ready to connect to Firestore.")
    real_json_data = [] 
else:
    print("No live database keys found yet. Running simulation mode instead...")
    
    # Live Firestore simulation batch based on your team's specification document
    firestore_json_data = """
    [
        {"timestamp": "2026-06-29 12:00:01", "temperature": 35.2, "humidity": 60, "current": 12.1, "voltage": 220.4, "power": 2.61, "vibration": 1.45},
        {"timestamp": "2026-06-29 12:00:02", "temperature": 36.1, "humidity": 59, "current": 11.9, "voltage": 219.8, "power": 2.58, "vibration": 1.52},
        {"timestamp": "2026-06-29 12:00:03", "temperature": 38.5, "humidity": 61, "current": 14.2, "voltage": 221.1, "power": 2.85, "vibration": 2.10},
        {"timestamp": "2026-06-29 12:00:04", "temperature": 35.0, "humidity": 60, "current": 12.0, "voltage": 220.0, "power": 2.60, "vibration": 1.40},
        {"timestamp": "2026-06-29 12:00:05", "temperature": 42.3, "humidity": 62, "current": 16.5, "voltage": 218.5, "power": 3.10, "vibration": 3.45}
    ]
    """
    real_json_data = json.loads(firestore_json_data)

print("-" * 40 + "\n")

# ==========================================================
# SECTION 2: DATAFRAME ANALYTICS PIPELINE
# ==========================================================
# This section remains completely UNTOUCHED when you get the real data.
df = pd.DataFrame(real_json_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 1. Inspect Data Shape
print("--- [1/4] DATASET SHAPE ---")
print(f"Total Database Records (Rows): {df.shape[0]}")
print(f"Total Telemetry Fields (Columns): {df.shape[1]}")
print("\n" + "-"*40 + "\n")

# 2. Inspect Data Types
print("--- [2/4] SENSOR DATA TYPES ---")
print(df.dtypes)
print("\n" + "-"*40 + "\n")

# 3. Inspect Sample Values
print("--- [3/4] SAMPLE VALUES (Telemetry Matrix) ---")
print(df)
print("\n" + "-"*40 + "\n")

# 4. Generate Summary Statistics
print("--- [4/4] GENERATING SUMMARY STATISTICS ---")
summary_stats = df.describe().T
print(summary_stats[['count', 'mean', 'std', 'min', 'max']])
print("\n" + "-"*40 + "\n")

# Export analytics table for team review
summary_stats.to_csv('live_telemetry_summary_statistics.csv')
print("Done! Analysis exported successfully to 'live_telemetry_summary_statistics.csv'")
print("==================================================")
