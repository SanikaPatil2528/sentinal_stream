import pandas as pd

from src.generator import generate_base_metrics
from src.anomalies import inject_point_anomalies, inject_memory_leak
from src.detector import SentinelDetector

print("🏁 Phase 2 Execution: Multi-Dimensional Verification")
print("=" * 60)

# Step 1: Generate clean training data using your function
print("📦 Step 1: Generating clean baseline traffic...")
df_clean = generate_base_metrics()

# Step 2: Train our multi-dimensional machine learning model
print("🌲 Step 2: Training Sentinel Detector on clean operational baseline...")
detector = SentinelDetector(contamination=0.02)
detector.fit(df_clean)

# Step 3: Generate a completely fresh dataset for testing evaluation
print("\n📦 Step 3: Generating fresh evaluation data matrix...")
df_final = generate_base_metrics()

# Step 4: Inject BOTH types of anomalies using your exact functional pipeline
print("💉 Injecting rapid flash spikes (Velocity Anomalies)...")
df_final = inject_point_anomalies(df_final)

print("💉 Injecting a gradual, creeping memory leak (Structural Trend)...")
df_final = inject_memory_leak(df_final)

# Step 5: Run the multi-dimensional prediction pipeline
print("\n🕵️‍♂️ Step 4: Running real-time inference pipeline across 15 dimensions...")
predictions = detector.predict(df_final)

# Append predictions back to the dataframe for final accounting
df_final['is_anomaly'] = predictions
total_rows = len(df_final)
detected_anomalies = (df_final['is_anomaly'] == -1).sum()

print("=" * 60)
print(f"📊 Assessment Complete!")
print(f"📈 Total Stream Intervals Evaluated: {total_rows} minutes")
print(f"🚨 Total Timestamps Isolated as Outliers: {detected_anomalies}")
print("=" * 60)