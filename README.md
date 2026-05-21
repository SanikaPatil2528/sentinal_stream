# SentinelStream: Early API Failure Detection System

An AI-powered AIOps monitoring pipeline designed to detect point anomalies (sudden spikes) and trend anomalies (memory leaks) in API metrics using unsupervised machine learning.

## 🚀 Project Overview
Traditional monitoring systems rely on static thresholds (e.g., alert if CPU > 90%). This project implements **unsupervised anomaly detection** and **time-series forecasting** to anticipate failures *before* they cause system downtime, while providing automated Root Cause Analysis (RCA).

## 🛠️ Tech Stack & Tools
- **Language:** Python 3.10+
- **Data Engineering:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (Isolation Forest)
- **Visualization:** Matplotlib

## 📁 Repository Structure
- `data/`: Local storage for generated telemetry datasets (ignored by Git).
- `models/`: Serialized trained machine learning models (ignored by Git).
- `src/`: Modular Python package containing the core pipeline logic.