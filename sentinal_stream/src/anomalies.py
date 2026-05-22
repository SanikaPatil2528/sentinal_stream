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
    Simulates a gradual, linear memory leak that begins randomly in the 
    latter portion of the dataset and steadily climbs until it forces a crash.
    """
    df_anomaly=df.copy()
    total_rows=len(df_anomaly)

    # Determine the starting row index for the leak (e.g.,around the 75% mark of the stream)
    start_idx=int(total_rows*start_fraction)
    # Linearly compound RAM usage minute-by-minute until it pushes past 95%+ 
    leak_slope=np.linspace(0,60,total_rows-start_idx) 
    # max base memory was 45+1.5=47.5 and after spike can rise upto 47.5+60 =107.5
    # if would have been (0,50) never crosses 98% mark in future code

    for i,idx in enumerate(range(start_idx,total_rows)):
        df_anomaly.loc[idx,'memory_utilization_pct']+=leak_slope[i]

        # Enforce physical maximum upper bound ceiling
        if df_anomaly.loc[idx,'memory_utilization_pct']>98.0:
            df_anomaly.loc[idx,'memory_utilization_pct']=98.0
    
    return df_anomaly