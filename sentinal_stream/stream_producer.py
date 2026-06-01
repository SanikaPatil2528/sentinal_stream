import socket
import time
import json
import pandas as pd

from src.generator import generate_base_metrics
from src.anomalies import inject_point_anomalies,inject_memory_leak


def create_simulation_warehouse():
    print("Initializing Simulation Data Warehouse...")
    
    # Generate 3 days of clean baseline metrics
    df=generate_base_metrics(days=3)
    df=inject_point_anomalies(df)
    df=inject_memory_leak(df)

    print(f"Warehouse ready with {len(df)} total minutes of simulation data!")
    return df


# Network Configuration
HOST = "127.0.0.1"  # Localhost - own computer
PORT = 9999  # The network port lane we will communicate through


def main():
    # 1. Load our data rows into memory
    df_warehouse=create_simulation_warehouse()
    print(f"Attempting to connect to the Consumer stream at {HOST}:{PORT}...")


    # 2. Create a raw TCP/IP streaming socket client

    # AF_INET means we are using standard IP addresses (IPv4).
    # SOCK_STREAM means we want a reliable, continuous stream of data where order is guaranteed (TCP), rather than loose packets that can arrive out of order (UDP).
    # with ... as client_socket: This is a Python context manager. It ensures that if our script crashes or stops, the operating system immediately safely closes the network port so it doesn't get jammed open.
    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket:
        try:
            # Connect the wire to our listener port 
            client_socket.connect((HOST,PORT))
            print("Connection established successfully! Stream is live.")

            # --- Transmission Loop---

            # 3. Iterate over every single row in our warehouse DataFrame
            for idx,row in df_warehouse.iterrows():
                # Convert the Pandas Series row into a clean, standard python dictionary
                row_dict=row.to_dict()

                # Convert the PAndas Timestamp object to an ISO string so the JSON serializer can process it without throwing an error
                row_dict['timestamp']=str(row_dict['timestamp'])

                # Transform the dictionary into a plain-text JSON string and add our newline delimiter
                # This is our signal flag so the consumer script knows exactly where one data packet ends and the next begins.
                json_string=json.dumps(row_dict) + "\n"  # dumps-> convert pthon obje (here dict) to json formatted string

                # Convert the plain text string into raw binary bytes using UTF-8
                binary_bytes=json_string.encode('utf-8')

                client_socket.sendall(binary_bytes)

                print(f"Sent row {idx+1}/{len(df_warehouse)} -> Time: {row_dict['timestamp']} | CPU: {row_dict['cpu_utilization_pct']:.1f}%")

                # Sleep for exactly 1 second to throttle our streaming speed
                time.sleep(1)


        except ConnectionRefusedError:
            print("\nConnection Failed!")
            print("Error:The consumer script isn't awake yet.")
            print("Reminder: You must start 'stream_consumer.py' FIRST so it can open the port, then start this Producer script second!")
            return 



if __name__=="__main__":
    main()