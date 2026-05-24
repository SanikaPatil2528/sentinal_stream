from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd


class SentinelDetector:
    def __init__(self,contamination=0.015,random_state=42):
        """
        Initializes the unsupervised Isolation Forest anomaly detector.
        
        Parameters:
        - contamination: The approximate proportion of outliers expected in the data.
        - random_state: Seed to ensure our random tree splits are reproducible.
        """
        self.contamination=contamination
        self.random_state=random_state

        self.model=IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=100, # number of decsion trees in forest
            n_jobs= -1 # uses all available CPU cores
            )
        
        self.base_metrics=[
            'requests_per_sec',
            'cpu_utilization_pct',
            'memory_utilization_pct',
            'latency_ms',
            'error_rate_pct'
        ]

        # The Raw Snapshot: What is happening right now.
        # The Velocity (5-Min Delta): How fast things are changing (to catch sudden spikes)
        self.delta_features=[f"{metric}_delta_5m" for metric in self.base_metrics]
        # The Structural Trend (10-Min Moving Average): How things are drifting over time (to catch slow, creeping failures like memory leaks).
        self.ma_features=[f"{metric}_ma_10m" for metric in self.base_metrics]

        # combined feature space (15 total numerical dimensions)
        self.feature_cols=self.base_metrics+self.delta_features+self.ma_features


    def _engineer_temporal_features(self,df:pd.DataFrame) -> pd.DataFrame:
        """
        Transforms raw data into a 3-part multi-dimensional vector per row.
        Processes data without mutating the original dataframe.
        """
        df_feats=df.copy()

        for metric in self.base_metrics:
            # Dimension A: Velocity (.diff calculates current minus 5 steps ago)
            # we fill the initial 5 NaN rows with 0.0 
            df_feats[f"{metric}_delta_5m"]=df_feats[metric].diff(periods=5).fillna(0.0)

            # Dimension B: Structural Trend (.rolling calculates the mean over a 10 step window)
            # min_periods=1 prevents NaN generation on early rows by averaging whatever is available
            df_feats[f"{metric}_ma_10m"]=df_feats[metric].rolling(window=10,min_periods=1).mean()
        
        return df_feats
    
    def fit(self,df_train:pd.DataFrame):
        """
        Trains the Isolation Forest on clean, healthy historical baseline data.
        """
        print("ML Engine: Engineering temporal signals for training dataset...")
        df_engineered=self._engineer_temporal_features(df_train)

        print("ML Engine: Training Isolation Forest on healthy baseline profile...")
        # Feed ONLY our numeric base metrics + temporal delta columns into the model
        X_train=df_engineered[self.feature_cols]
        self.model.fit(X_train)
        print("ML Engine: Training complete! Normal behavior baseline established.")

        return self
    
    def predict(self,df_input:pd.DataFrame) -> np.ndarray:
       """
        Evaluates an incoming dataset on the fly and returns anomaly vector mappings.
        Outputs: 1 for normal data points, -1 for anomalous data points.
        """
       df_engineered=self._engineer_temporal_features(df_input)
       X_inference=df_engineered[self.feature_cols]
       return self.model.predict(X_inference)