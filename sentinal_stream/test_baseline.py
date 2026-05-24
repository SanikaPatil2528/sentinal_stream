from src.generator import generate_base_metrics
from src.anomalies import inject_point_anomalies, inject_memory_leak

print("🔄 Step 1: Generating clean baseline data...")
df_clean = generate_base_metrics(days=1)

print("💥 Step 2: Injecting random point spikes...")
df_spiked = inject_point_anomalies(df_clean, probability=0.01)

print("📈 Step 3: Injecting the slow system memory leak...")
df_final = inject_memory_leak(df_spiked)

print("\n✅ Verification Successful!")
print(f"📊 Rows Processed: {len(df_final)}")
print(f"🧠 Clean RAM Max: {df_clean['memory_utilization_pct'].max():.2f}%")
print(f"🚨 Leaked RAM Max: {df_final['memory_utilization_pct'].max():.2f}%")

# Let's count how many rows got mutated by point spikes
monitored_metrics = ['requests_per_sec', 'cpu_utilization_pct', 'latency_ms', 'error_rate_pct']

# 2. Check where the clean data does not equal the spiked data across all these columns
# .any(axis=1) checks if AT LEAST one column in a row was mutated
total_mutated_rows = (df_clean[monitored_metrics] != df_spiked[monitored_metrics]).any(axis=1).sum()

print(f"🎯 Total Randomized Point Anomalies Generated: {total_mutated_rows} spikes across the timeline.")