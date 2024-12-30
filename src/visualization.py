import matplotlib.pyplot as plt
import os

class Visualizer:
    def __init__(self):
        self.output_dir = 'visualizations'
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_metrics_with_anomalies(self, data, anomalies, metric_type):
        """Create visualizations of metrics with anomaly highlighting"""
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
        
        for column in numeric_columns:
            if column == 'timestamp':
                continue
                
            plt.figure(figsize=(12, 6))
            
            # Plot for each host
            for host in data['host'].unique():
                host_data = data[data['host'] == host]
                plt.plot(
                    host_data['timestamp'], 
                    host_data[column], 
                    label=f'{host} - {column}'
                )
            
            # Highlight anomalies if detected
            if anomalies.get(column, False):
                plt.axvspan(
                    data['timestamp'].iloc[-60],
                    data['timestamp'].iloc[-1],
                    color='red',
                    alpha=0.3,
                    label='Anomaly'
                )
            
            plt.title(f'{column} Over Time')
            plt.xlabel('Time')
            plt.ylabel(column)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            filename = f"{metric_type}_{column.lower().replace(' ', '_')}.png"
            plt.savefig(os.path.join(self.output_dir, filename))
            plt.close()

    def create_all_visualizations(self, data_dict, anomalies_dict):
        """Create visualizations for all metrics"""
        for metric_type, data in data_dict.items():
            self.plot_metrics_with_anomalies(
                data, 
                anomalies_dict.get(metric_type, {}),
                metric_type
            )