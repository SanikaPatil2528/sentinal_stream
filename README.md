# SentinelStream: Early API Failure Detection System

An AI-powered AIOps monitoring pipeline designed to detect point anomalies (sudden spikes) and trend anomalies (memory leaks) in API metrics using unsupervised machine learning.

## 🚀 Project Overview
Traditional monitoring systems rely on static thresholds (e.g., alert if CPU > 90%). This project implements **unsupervised anomaly detection** and **time-series forecasting** to anticipate failures *before* they cause system downtime, while providing automated Root Cause Analysis (RCA).

## 🛠️ Tech Stack & Tools
- **Language:** Python 3.10+
- **Data Stream Framework:** Socket (TCP/IP Streams)
- **Data Engineering:** Pandas, NumPy, Collections (Deque)
- **Machine Learning:** Scikit-Learn (Isolation Forest), Joblib
- **Visualization:** Matplotlib

## 📁 Repository Structure
- `data/`: Local storage for generated telemetry datasets (ignored by Git).
- `models/`: Serialized trained machine learning models (ignored by Git).
- `src/`: Modular Python package containing the core pipeline logic.
- `stream_producer.py`: Simulation engine generating live infrastructure logs.
- `stream_consumer.py`: Edge-computing analytics consumer and diagnostic engine.

---

## 🏗️ System Architecture

The project implements a classic **decoupled Publisher-Subscriber (Producer-Consumer) topology** over raw TCP/IP sockets, mimicking enterprise edge-telemetry collection.



============================================================================================

+-----------------------------------+
|      Infrastructure Producer      |  <-- Simulates live cluster telemetry
+-----------------------------------+
│
▼  (Streaming JSON Packets over TCP/IP)
+-----------------------------------+
|       Stream Consumer Core        |  <-- Reads socket line-by-line
+-----------------------------------+
│
▼
+-----------------------------------+
|    Sliding History Buffer         |  <-- Maintains rolling 10-interval context
|         (Python deque)            |
+-----------------------------------+
│
┌────────┴────────┐
▼                 ▼
[ TRACK 1: SPIKES ]   [ TRACK 2: DRIFTS ]
+-----------------+   +------------------+
| IsolationForest |   | Rolling Calculus |
| Machine Learning|   | Velocity Engine  |
+-----------------+   +------------------+
│                 │
└────────┬────────┘
▼
+-----------------------------------+
|    Root Cause Diagnosis Engine    |  <-- Statistical distance fingerprinting
+-----------------------------------+
│
▼
+-----------------------------------+
|   Predictive Warning Console      |  <-- Alerts with dynamic Time-To-Failure
+-----------------------------------+

============================================================================================

---

## 🔬 Core Analytical Framework

To eliminate alert fatigue and ensure continuous tracking, the system evaluates incoming data across two independent geometric dimensions:

### Track 1: Volatile Point Anomalies (Isolation Forest)
For unpredictable, erratic metrics like **CPU Utilization**, **Network Latency**, and **Error Rates**, the system feeds a structured temporal sliding dataframe into a frozen **Isolation Forest** model. 

Because sudden microservice failures or network shocks represent data coordinates vastly distant from dense clusters of normal behavior, the tree structures isolate them immediately, yielding a fast, unsupervised anomaly score of `-1` without requiring manual threshold adjustments.

### Track 2: Accumulative Trend Anomalies (Streaming Calculus)
Slow, creeping structural degradations—such as a developer forgetting to clear a memory cache—under-run standard machine learning boundaries day-to-day. SentinelStream overrides this blind spot by running continuous velocity calculations over the historical window.

#### 1. Consumption Velocity ($\text{Velocity}_{\text{mem}}$)
The system calculates the linear slope of resource consumption across the sliding window:
$$\text{Velocity}_{\text{mem}} = \frac{M_{\text{current}} - M_{\text{oldest}}}{N - 1}$$
*Where $M$ represents memory utilization and $N$ represents the window capacity (10 rows).*

#### 2. Resource Headroom ($\text{Headroom}_{\text{mem}}$)
The buffer ceiling distance remaining before a catastrophic Operating System Out-Of-Memory (OOM) process termination:
$$\text{Headroom}_{\text{mem}} = 100.0\% - M_{\text{current}}$$

#### 3. Predictive Time-To-Failure ($\text{TTF}$)
If the consumption velocity breaches our noise filter ($\text{Velocity} > 0.05\%$), the engine divides remaining headroom by current trajectory speed to project an accurate, production-grade operational warning window:
$$\text{TTF}_{\text{minutes}} = \frac{\text{Headroom}_{\text{mem}}}{\text{Velocity}_{\text{mem}}}$$

---

## 🛠️ Automated Root Cause Fingerprinting (RCA)

When an anomaly is flagged by either track, the system extracts the statistical mean of the sliding window ($\mu$) and executes dynamic distance heuristic checks to isolate the precise failure topology:

| Failure Mode Identity | Mathematical Condition | Real-World Operational Context |
| :--- | :--- | :--- |
| **Resource Exhaustion (Memory Leak)** | $M_{\text{live}} > \mu_{M} + 8.0$ <br> $\text{Req}_{\text{live}} \le \mu_{\text{Req}} \times 1.2$ | Application is bleeding memory internally while processing a flat, non-spiking volume of standard consumer traffic. |
| **Downstream API Failure** | $\text{Err}_{\text{live}} > \mu_{\text{Err}} + 5.0$ | Core resources look healthy, but external API network integrations or database pools have suddenly snapped. |
| **Network Traffic Surge (DDoS)** | $\text{Req}_{\text{live}} > \mu_{\text{Req}} \times 1.5$ | Server CPU and latency are choking due to an external concurrent flood of incoming requests or botnet stress events. |

---

## 🚀 Commercial Scaling & Hardening Roadmap (System Design)

To transform this lightweight single-node proof-of-concept into a massive multi-region enterprise platform, the following design scaling patterns are recommended:

1. **Distributed Event Backbone:** Swap out raw TCP/IP sockets for **Apache Kafka** or **AWS Kinesis**. This decouples ingestion, introduces durable disk-backed offsets, and allows multiple parallel consumer threads to process thousands of server logs concurrently.
2. **State Persistence Caching:** Migrate the local Python in-memory `deque` state to a high-speed time-series storage layer like **Prometheus** or **InfluxDB**. This ensures that if the analytical consumer script crashes, it can instantly re-hydrate its historical history window upon restart without creating operational blind spots.
3. **MLOps Continuous Training:** Implement an automated retraining orchestrator using **MLflow**. Telemetry profiles drift when developers ship new software updates; tracking model performance against production baselines ensures the Isolation Forest continuously adapts without generating false alarms.