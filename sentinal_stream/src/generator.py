import pandas as pd
import numpy as np


def generate_base_metrics(days=1,interval_min=1):
    """
    Generates clean, normal, healthy baseline telemetry data for an API.
    Simulates diurnal traffic cycles, metric correlations, and system noise.
    """
    ## 24 hours * 60 min = 1440 points per day
    total_points=int((days*24*60)/interval_min)
    timestamps=pd.date_range(start="2026-05-21 00:00",periods=total_points,freq=f"{interval_min}min")

    ## 1. model a smooth diurnal(day/night) traffic cycle using sine wave
    # generates ARRAY (start,end,no.of points) 2pi to make it complete for the whole day (360 degree)
    time_axis=np.linspace(0,2*np.pi*days,total_points)
    # shifting the wave upward, so that it remains positive --> The sine wave swings smoothly, creating traffic that ranges between 20 and 80 req/sec
    base_traffic=50+30*np.sin(time_axis-np.pi/2)

    ## 2. add random Gaussian noise (mean=0, sd=4) to make traffic look organic
    requests=base_traffic+np.random.normal(0,4,total_points)
    requests=np.clip(requests,5,None) # traffic cant drop below 5

    ## 3. build correlated system metrics based on traffic volume

    # CPU Usage climbs directly with traffic load
    cpu_utilization=(requests*0.5)+np.random.normal(15,2,total_points)
    # Network response latency(in ms) increases as traffic load builds
    latency_ms=(requests*0.8)+np.random.normal(20,3,total_points)
    # on a healthy server, RAM utilization stays flat,steady, and unaffected by traffic spikes
    memory_utilization=np.random.normal(45,1.5,total_points)
    # API error rate remains low and stable under normal operating conditions
    error_rate=np.random.uniform(0.1,1.0,total_points)

    data={
        'timestamp':timestamps,
        'request_per_sec':requests,
        'cpu_utilization_pct':np.clip(memory_utilization,0,100),
        'latencyy_ms':np.clip(latency_ms,0,None),
        'error_rate_pct':np.clip(error_rate,0,100)
    }

    return pd.DataFrame(data)