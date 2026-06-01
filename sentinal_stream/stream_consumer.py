# socket: To host our network server port.

# json: To decode incoming bytes back into readable Python dictionaries.

# collections.deque: Our core sliding memory buffer.

# pandas: To structure the deque into a clean dataframe for instant rolling feature math.

# joblib: To load our frozen model brain into active RAM.

import socket
import json
from collections import deque
import pandas as pd
import joblib
from src.detector import SentinelDetector


HOST="127.0.0.1"
PORT=9999

def load_ml_model():
    model_path="models/sentinel_model.joblib"
    print(f"Loading frozen ML model from {model_path}...")
    try:
        model=joblib.load(model_path)
        print(f"Model successfully loadeed into memory and ready for inference!")
        return model
    except FileNotFoundError:
        print(f"\n Error: Could not find your model file at '{model_path}'")
        print("Reminder: Make sure you ran 'test_detector.py' previously to save the model asset.")
        return None


def main():
    # Step 1: Load model
    model=load_ml_model()
    if model is None:
        return 
    
    detector=SentinelDetector()

    # Step 2: Initialize memory buffer
    memory_buffer=deque(maxlen=10)
    print(f"Sliding memory window initialized (Size: {memory_buffer.maxlen} rows).")

    # Step 3: Create a raw TCP/IP streaming socket server
    print(f"Opening server port lane... Listening at {HOST}:{PORT}")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST,PORT))
        server_socket.listen(1) 
        print("Server is awake and actively waiting for the Producer to connect...")

        conn,addr=server_socket.accept()
        with conn:
            print(f"Connected by live data stream pipeline from: {addr}\n")

            # Create a network file-like reader to cleanly stream data line by line
            reader=conn.makefile('r',encoding='utf-8')

            for line in reader:
                # Strip any stray spacing and skip empty lines
                clean_line=line.strip()
                if not clean_line:
                    continue

                # Decode the raw text string back into a python dictionary
                metrics_packet=json.loads(clean_line)

                # Push the new packet into our rolling 60-row memory buffer
                memory_buffer.append(metrics_packet)

                # Wait until we have a full 10-row window so the moving average is true and stable
                if len(memory_buffer)<10:
                    print(f"Buffering history... ({len(memory_buffer)}/60 rows loaded)", end="\r")
                    continue

                # Step 4: Transform the memory window into a DataFrame for feature engineering
                df_window=pd.DataFrame(list(memory_buffer))

                df_engineered=detector._engineer_temporal_features(df_window)

                latest_features=df_engineered.iloc[[-1]]

                # Filter down to exact training columns subset matching your Isolation Forest features
                X_inference=latest_features[detector.feature_cols]

                # Step 5: Make the inference prediction
                prediction=model.predict(X_inference)[0] ## o/p is as [-1] so grab it with [0] in list

                # Step 6: Clear and readable tracking output
                timestamp=metrics_packet.get('timestamp','UNKNOWN')
                
                # Grab and format metrics to 1 decimal place for clean reading
                cpu = float(metrics_packet.get('cpu_utilization_pct', 0))
                latency = float(metrics_packet.get('latency_ms', 0))
                error = float(metrics_packet.get('error_rate_pct', 0))

                if prediction == -1:
                    print(f"\n🚨 [ANOMALY DETECTED] at {timestamp}!")
                    print(f"   CPU: {cpu:.1f}% | Latency: {latency:.1f}ms | Error: {error:.1f}%")
                    print("-" * 60)
                else:
                    # 💡 Trick: Adding '\033[K' clears any leftover characters from the previous line 
                    # when using '\r', ensuring it never looks jumbled!
                    print(f"🟢 [NORMAL] {timestamp} - CPU: {cpu:.1f}% | Latency: {latency:.1f}ms\033[K", end="\r")


if __name__=="__main__":
    main()