import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# InfluxDB Configuration
INFLUXDB_CONFIG = {
    'host': os.getenv('INFLUXDB_HOST'),
    'token': os.getenv('INFLUXDB_TOKEN'),
    'org': os.getenv('INFLUXDB_ORG'),
    'bucket': os.getenv('INFLUXDB_DATABASE')
}

# Vector DB Configuration
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_db')

# Anomaly Detection Configuration
ANOMALY_CONFIG = {
    'vector_size': 10,  # Number of dimensions for vector representation
    'window_size': 100,  # Number of data points to consider for each pattern
    'similarity_threshold': 0.8  # Threshold for determining anomalies
}

# Data file paths
DATA_PATHS = {
    'system': 'data/system-metrics-data.csv',
    'application': 'data/application-metrics-data.csv',
    'network': 'data/network-metrics-data.csv'
}