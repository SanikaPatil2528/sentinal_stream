import pandas as pd
import os
import joblib

from src.generator import generate_base_metrics
from src.anomalies import inject_point_anomalies, inject_memory_leak
from src.detector import SentinelDetector

print("🏁 Phase 2 Execution: Multi-Dimensional Verification")
print("=" * 60)

# Step 1: Generate clean training data using your function
print("📦 Step 1: Generating clean baseline traffic...")
df_clean = generate_base_metrics(days=7)

# Step 2: Train our multi-dimensional machine learning model
print("🌲 Step 2: Training Sentinel Detector on clean operational baseline...")
detector = SentinelDetector(contamination=0.02)
detector.fit(df_clean)


## FREEZING AND SAVING THE TRAINED ENGINE
print("\nSentinel Engine: Freezing and saving the trained model...")

os.makedirs("models",exist_ok=True)
model_path="models/sentinel_model.joblib"
joblib.dump(detector,model_path,compress=3)

print(f"SUCCESS: Trained brain asset securely saved to ''{model_path}'!")
print("="*60)


## CRITICAL SANITY CHECK: Wipe the original model object from RAM
del detector
print("Original live model wiped from RAM to guarantee file verification.")
print("="*60)




## LOADING THE MODEL FRESH FROM THE JOBLIB FILE
print("\nLoading model asset fresh from the saved disk file...")
loaded_detector=joblib.load(model_path)
print("\nSUCCESS: Model loaded into 'loaded_detector' asset!")
print("="*60)





# Step 3: Generate a completely fresh dataset for testing evaluation
print("\nStep 3: Generating fresh evaluation data matrix...")
df_final=generate_base_metrics()

# Step 4: Inject both type of anomalies
print("\nInjecting rapid flash spikes (Velocity Anomalies)...")
df_final=inject_point_anomalies(df_final)

print("\nInjecting a gradual, creeping memory leak (Structural Trend)...")
df_final=inject_memory_leak(df_final)

# Step 5: Run the multi-dimensional prediction pipeline using the loaded model
print("\nStep 5: Running real-time inference pipeline across dimensions using LOADED asset...")
predictions=loaded_detector.predict(df_final)

# Append predictions back to data frame for final accounting
df_final['is_anomaly']=predictions
total_rows=len(df_final)
detected_anomalies=(df_final['is_anomaly']==-1).sum()

print("="*60)
print(f"Assessment Complete!")
print(f"Total Stream Intervals Evaluated: {total_rows} minutes")
print(f"Total Timestamps Isolated as Outliers: {detected_anomalies}")
print("="*60)