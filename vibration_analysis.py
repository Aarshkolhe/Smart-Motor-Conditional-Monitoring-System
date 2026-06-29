import json
import os
import matplotlib
# Use a background rendering engine to prevent terminal lockups on Windows
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("        COMBINED DATA ANALYTICS PIPELINE          ")
print("==================================================")
print("\n")

# ==========================================================
# 🛑 SECTION 1: DATABASE CONFIGURATION & SWITCH LOGIC
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

# Check if live cloud database keys are present yet
if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Ready to connect to Firestore.")
    real_json_data = [] 
else:
    print("No live database keys found yet. Running simulation mode instead...")
    
    # Combined master simulation batch containing all primary spec sensors and targets
    firestore_json_data = """
    [
        {"timestamp": "2026-06-29 12:00:01", "temperature": 35.2, "humidity": 60, "current": 12.1, "voltage": 220.4, "power": 2.61, "healthy_vib": 1.12, "faulty_vib": 3.42},
        {"timestamp": "2026-06-29 12:00:02", "temperature": 36.1, "humidity": 59, "current": 11.9, "voltage": 219.8, "power": 2.58, "healthy_vib": 1.25, "faulty_vib": 3.81},
        {"timestamp": "2026-06-29 12:00:03", "temperature": 38.5, "humidity": 61, "current": 14.2, "voltage": 221.1, "power": 2.85, "healthy_vib": 1.08, "faulty_vib": 4.12},
        {"timestamp": "2026-06-29 12:00:04", "temperature": 35.0, "humidity": 60, "current": 12.0, "voltage": 220.0, "power": 2.60, "healthy_vib": 1.19, "faulty_vib": 5.25},
        {"timestamp": "2026-06-29 12:00:05", "temperature": 42.3, "humidity": 62, "current": 16.5, "voltage": 218.5, "power": 3.10, "healthy_vib": 1.31, "faulty_vib": 6.90}
    ]
    """
    real_json_data = json.loads(firestore_json_data)

print("-" * 40 + "\n")

# ==========================================================
# 📊 SECTION 2: DATAFRAME ANALYTICS & PROFILING
# ==========================================================
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

# Export analytics data grid to a text table format file
summary_stats.to_csv('live_telemetry_summary_statistics.csv')
print("Done! Analysis exported successfully to 'live_telemetry_summary_statistics.csv'")
print("-" * 40 + "\n")

# ==========================================================
# 📈 SECTION 3: AUTOMATED TIME-SERIES VISUALIZATION
# ==========================================================
print("Generating unified vibration profile chart...")

# Create a single drawing canvas window
plt.figure(figsize=(12, 6))

# Generate continuous baseline numeric sequence for the X-axis timeline
time_indices = range(len(df))

# Plot BOTH lines on the exact same single canvas plot
plt.plot(time_indices, df['healthy_vib'], color='teal', linewidth=2.5, marker='o', label='Healthy Baseline (Stable)')
plt.plot(time_indices, df['faulty_vib'], color='crimson', linewidth=2.5, marker='x', label='Faulty Stream (Bearing Anomaly)')

# Horizontal safety limit thresholds for anomaly validation
plt.axhline(y=2.5, color='orange', linestyle=':', linewidth=1.5, label='Warning Limit (2.5 mm/s)')
plt.axhline(y=5.0, color='red', linestyle=':', linewidth=1.5, label='Critical Failure Limit (5.0 mm/s)')

# Chart Labels & Aesthetics
plt.title('Motor Telemetry Profile: Healthy vs. Faulty Vibration Comparison', fontsize=13, fontweight='bold')
plt.xlabel('Telemetry Stream Window Sequence', fontsize=11)
plt.ylabel('Vibration Amplitude (mm/s)', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.ylim(0, 10)
plt.legend(loc='upper left', fontsize=10)

# Adjust padding and layout frame
plt.tight_layout()

# Save the unified comparison chart to your workspace
output_image = 'live_vibration_comparison.png'
plt.savefig(output_image, dpi=300, bbox_inches='tight')
print(f"Success! Combined comparison plot generated: '{output_image}'")
print("==================================================")
