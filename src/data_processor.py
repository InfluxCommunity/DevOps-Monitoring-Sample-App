from influxdb_client_3 import InfluxDBClient3, Point
from src.config import INFLUXDB_CONFIG, DATA_PATHS
import pandas as pd

class DataProcessor:
    def __init__(self):
        self.client = InfluxDBClient3(
            token=INFLUXDB_CONFIG['token'],
            host=INFLUXDB_CONFIG['host'],
            org=INFLUXDB_CONFIG['org'],
            database=INFLUXDB_CONFIG['bucket']  # bucket name in InfluxDB Cloud
        )

    def load_data(self):
        """Load data from CSV files"""
        data = {}
        for key, path in DATA_PATHS.items():
            data[key] = pd.read_csv(path)
            data[key]['timestamp'] = pd.to_datetime(data[key]['timestamp'])
        return data

    def write_to_influxdb(self, data):
        """Write data to InfluxDB"""
        for metric_type, df in data.items():
            try:
                # Using the Pandas DataFrame write method
                self.client._write_api.write(
                    bucket=INFLUXDB_CONFIG['bucket'],
                    record=df,
                    data_frame_measurement_name=metric_type,
                    data_frame_tag_columns=['host'],
                    data_frame_timestamp_column='timestamp'
                )
                print(f"Successfully wrote data for {metric_type}")
            except Exception as e:
                print(f"Error writing {metric_type} data: {e}")

    def query_data(self, metric_type, hours=1):
        """Query data from InfluxDB using SQL"""
        query = f"""
        SELECT * FROM {metric_type}
        WHERE time >= now() - {hours}h
        """
        
        try:
            reader = self.client.query(query=query, language="sql")
            table = reader.read_all()
            return table.to_pandas()
        except Exception as e:
            print(f"Error querying {metric_type} data: {e}")
            return None

    def process(self):
        """Main processing function"""
        print("Loading data from CSV files...")
        data = self.load_data()
        
        print("Writing data to InfluxDB...")
        self.write_to_influxdb(data)
        
        return data