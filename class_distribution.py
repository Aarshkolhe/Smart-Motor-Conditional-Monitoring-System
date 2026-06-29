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
print("          TASK 4: CLASS DISTRIBUTION ENGINE       ")
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
    # Simulated specification-accurate dataset containing realistic imbalanced fault targets
    firestore_json_data = """
    [
        {"fault_type": "Normal"}, {"fault_type": "Normal"}, {"fault_type": "Normal"},
        {"fault_type": "Normal"}, {"fault_type": "Normal"}, {"fault_type": "Normal"},
        {"fault_type": "Normal"}, {"fault_type": "Normal"}, {"fault_type": "Normal"},
        {"fault_type": "Normal"}, {"fault_type": "Normal"}, {"fault_type": "Normal"},
        {"fault_type": "Normal"}, {"fault_type": "Normal"}, {"fault_type": "Normal"},
        {"fault_type": "Bearing Failure"}, {"fault_type": "Bearing Failure"},
        {"fault_type": "Shaft Misalignment"}, {"fault_type": "Insulation Degradation"},
        {"fault_type": "Normal"}
    ]
    """
    real_json_data = json.loads(firestore_json_data)

# Load into active Pandas dataframe matrix 
df = pd.DataFrame(real_json_data)

# ==========================================================
# 2. QUANTIFY AND AUDIT TARGET CLASS IMBALANCE
# ==========================================================
print("\n--- AUDITING TARGET CLASS DISTRIBUTIONS ---")

# Calculate absolute raw counts per unique fault type
class_counts = df['fault_type'].value_counts()

# Calculate relative proportions / percentages for documentation
class_proportions = df['fault_type'].value_counts(normalize=True) * 100

# Combine them into a highly scannable report data frame for your senior
distribution_report = pd.DataFrame({
    'Raw_Sample_Count': class_counts,
    'Percentage_Proportion': class_proportions
})

print(distribution_report)
print("-" * 40)

# Export the report directly as a physical reference log table
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'class_imbalance_report.csv')
distribution_report.to_csv(report_path)
print(f"✅ Distribution audit logs saved to: '{report_path}'")

# ==========================================================
# 3. GENERATE TARGET DISTRIBUTION PLOTS
# ==========================================================
print("\nGenerating target class imbalance visualization...")
plt.figure(figsize=(10, 5))

# Create a clean categorical countplot tracking absolute frequencies
sns.countplot(data=df, x='fault_type', order=class_counts.index, palette='viridis')

# Chart Details, Formatting & Typography
plt.title('Industrial Telemetry: Target Class Fault Imbalance Profile', fontsize=13, fontweight='bold')
plt.xlabel('Motor Operating Classification/Fault Type', fontsize=11)
plt.ylabel('Total Collected Sample Count', fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Calculate forced path to ensure it drops directly into the inner repository folder on autopilot
script_dir = os.path.dirname(os.path.abspath(__file__))
image_save_path = os.path.join(script_dir, 'fault_class_distribution.png')

plt.savefig(image_save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Success! Visualization exported natively to: '{image_save_path}'")
print("==================================================")
