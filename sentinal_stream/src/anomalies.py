import numpy as np
import pandas as pd

def inject_point_anomalies(df,probability=0.01):
    """
    Randomly injects sudden, short-lived spikes (point anomalies) 
    into random metrics across the timeline based on a probability threshold.
    """
    df_anomaly=df.copy()
    metrics_to_spike=['requests_per_sec','cpu_utilization_pct','latency_ms','error_rate_pct']

    for idx in range(len(df_anomaly)):
        if np.random.rand()<probability:
            # randomly select which metric to break for this specific minute
            chosen_metric=np.random.choice(metrics_to_spike)

            # multiply metric by a random heavy factor(3x to 5x)
            spike_factor=np.random.uniform(3.0,5.0)
            df_anomaly.loc[idx,chosen_metric]*=spike_factor

            # post-spike logical correction
            if 'pct' in chosen_metric:
                df_anomaly.loc[idx,chosen_metric]=np.clip(df_anomaly.loc[idx,chosen_metric],0,100)
    
    return df_anomaly


def inject_memory_leak(df,start_fraction=0.75):
    """
    Simulates a completely randomized, gradual memory leak.
    It begins at a random time in the latter half of the day
    and climbs at a completely random rate.
    """
    df_anomaly=df.copy()
    total_rows=len(df_anomaly)

    # RANDOMIZATION 1: Pick a random starting point between 50% and 85% of the day
    random_start_fraction = np.random.uniform(0.50, 0.85)
    start_idx = int(total_rows * random_start_fraction)

    # RANDOMIZATION 2: Pick a random max leak severity between 40% and 75% RAM inflation
    random_max_leak = np.random.uniform(40.0, 75.0)

    # Generate the linear slope using our randomized limits
    remaining_minutes = total_rows - start_idx
    leak_slope = np.linspace(0, random_max_leak, remaining_minutes)

    # Inject the randomized leak into the timeline
    for i, idx in enumerate(range(start_idx, total_rows)):
        df_anomaly.loc[idx, 'memory_utilization_pct'] += leak_slope[i]

        # Enforce physical maximum upper bound ceiling
        if df_anomaly.loc[idx, 'memory_utilization_pct'] > 98.0:
            df_anomaly.loc[idx, 'memory_utilization_pct'] = 98.0
    
    return df_anomaly