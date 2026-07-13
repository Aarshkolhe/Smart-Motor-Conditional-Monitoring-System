import json
import os
import matplotlib
# Force background rendering engine to completely eliminate terminal pop-up freezes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_selection import f_classif, mutual_info_classif

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("          TASK 8: FEATURE IMPORTANCE ENGINE       ")
print("==================================================")
print("\n")

# ==========================================================
# 1. DATA INGESTION ENGINE (AUTOPILOT CONNECTIVITY ACTIVE)
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Initializing cloud dataset extraction...")
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
    
    # Simulated specification-accurate dataset containing realistic sensor-to-fault patterns
    firestore_json_data = """
    [
        {"temperature": 35.2, "humidity": 60, "current": 12.1, "vibration": 1.45, "fault_type": "Normal"},
        {"temperature": 36.1, "humidity": 59, "current": 11.9, "vibration": 1.52, "fault_type": "Normal"},
        {"temperature": 55.5, "humidity": 61, "current": 14.2, "vibration": 5.10, "fault_type": "Bearing Failure"},
        {"temperature": 35.0, "humidity": 60, "current": 12.0, "vibration": 1.40, "fault_type": "Normal"},
        {"temperature": 58.3, "humidity": 62, "current": 16.5, "vibration": 6.45, "fault_type": "Bearing Failure"},
        {"temperature": 34.8, "humidity": 60, "current": 11.8, "vibration": 1.38, "fault_type": "Normal"},
        {"temperature": 36.5, "humidity": 58, "current": 12.4, "vibration": 1.60, "fault_type": "Normal"},
        {"temperature": 54.2, "humidity": 65, "current": 19.8, "vibration": 5.80, "fault_type": "Bearing Failure"},
        {"temperature": 58.1, "humidity": 66, "current": 21.2, "vibration": 6.22, "fault_type": "Bearing Failure"},
        {"temperature": 62.4, "humidity": 68, "current": 23.5, "vibration": 7.45, "fault_type": "Bearing Failure"}
    ]
    """
    real_json_data = json.loads(firestore_json_data)

# Load data matrix
df = pd.DataFrame(real_json_data)

# Separate input features (X) and target categorical classification labels (y)
feature_cols = ['temperature', 'humidity', 'current', 'vibration']
X = df[feature_cols]
y = df['fault_type']

print(f"Dataset compiled: Evaluating {len(feature_cols)} features against target classes.")
print("-" * 40 + "\n")

# ==========================================================
# 2. COMPUTE STATISTICAL SCORES (ANOVA & MUTUAL INFORMATION)
# ==========================================================
print("Running ANOVA F-score and Mutual Information algorithms...")

# Calculate ANOVA F-values
f_scores, p_values = f_classif(X, y)

# Calculate Mutual Information scores (Set fixed seed for consistency)
mi_scores = mutual_info_classif(X, y, random_state=42)

# Combine results into a clean, unified ranking report DataFrame
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'ANOVA_F_Score': f_scores,
    'Mutual_Information_Score': mi_scores
}).sort_values(by='Mutual_Information_Score', ascending=False)

print("\n--- FEATURE IMPORTANCE SCORES RANKING ---")
print(importance_df.to_string(index=False))
print("-" * 40 + "\n")

# Export metrics directly into your repository folder
script_directory = os.path.dirname(os.path.abspath(__file__))
report_path = os.path.join(script_directory, 'feature_importance_report.csv')
importance_df.to_csv(report_path, index=False)
print(f"Success! Importance logs saved cleanly to: '{report_path}'")

# ==========================================================
# 3. GENERATE PLOTS (SIDE-BY-SIDE SIDEBAR SCORES)
# ==========================================================
print("Rendering feature scores visual profile layout...")
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))

# Plot A: ANOVA Scores Ranking
sns.barplot(data=importance_df.sort_values(by='ANOVA_F_Score', ascending=False), 
            x='ANOVA_F_Score', y='Feature', palette='plasma', ax=ax1)
ax1.set_title('Feature Ranking via ANOVA F-Score', fontsize=12, fontweight='bold')
ax1.set_xlabel('F-Score Value')
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# Plot B: Mutual Information Scores Ranking
sns.barplot(data=importance_df, x='Mutual_Information_Score', y='Feature', palette='viridis', ax=ax2)
ax2.set_title('Feature Ranking via Mutual Information', fontsize=12, fontweight='bold')
ax2.set_xlabel('Information Gain Score')
ax2.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()

image_save_path = os.path.join(script_directory, 'feature_importance_comparison.png')
plt.savefig(image_save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Success! Visual chart profile exported natively to: '{image_save_path}'")
print("==================================================")
