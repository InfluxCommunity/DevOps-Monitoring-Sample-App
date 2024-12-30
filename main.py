from src.data_processor import DataProcessor
from src.anomaly_detector import AnomalyDetector
from src.visualization import Visualizer

def main():
    # Initialize components
    processor = DataProcessor()
    detector = AnomalyDetector()
    visualizer = Visualizer()
    
    try:
        # Process data
        print("Processing metrics data...")
        data_dict = processor.process()
        
        # Detect anomalies
        print("Detecting anomalies...")
        anomalies_dict = {}
        for metric_type, data in data_dict.items():
            anomalies_dict[metric_type] = detector.detect_anomalies(data, metric_type)
        
        # Create visualizations
        print("Creating visualizations...")
        visualizer.create_all_visualizations(data_dict, anomalies_dict)
        
        print("Processing complete! Check the 'visualizations' directory for results.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()