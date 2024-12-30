from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
from sklearn.preprocessing import StandardScaler
from .config import VECTOR_DB_PATH, ANOMALY_CONFIG

class AnomalyDetector:
    def __init__(self):
        self.client = QdrantClient(path=VECTOR_DB_PATH)
        self.scaler = StandardScaler()
        self._initialize_collections()

    def _initialize_collections(self):
        """Initialize vector database collections"""
        for metric_type in ['system', 'application', 'network']:
            try:
                self.client.create_collection(
                    collection_name=f"{metric_type}_patterns",
                    vectors_config=models.VectorParams(
                        size=ANOMALY_CONFIG['vector_size'],
                        distance=models.Distance.COSINE
                    )
                )
            except Exception as e:
                print(f"Collection {metric_type}_patterns already exists or error: {e}")

    def create_pattern_vector(self, data, metric_name):
        """Convert metric window into vector representation"""
        values = data[metric_name].values[-ANOMALY_CONFIG['window_size']:]
        if len(values) < ANOMALY_CONFIG['window_size']:
            return None
            
        # Reshape and normalize
        normalized = self.scaler.fit_transform(values.reshape(-1, 1))
        
        # Reduce dimensionality by averaging windows
        window_size = len(normalized) // ANOMALY_CONFIG['vector_size']
        vector = np.array([
            normalized[i:i+window_size].mean() 
            for i in range(0, len(normalized), window_size)
        ])
        
        return vector

    def detect_anomalies(self, data, metric_type):
        """Detect anomalies in metrics"""
        anomalies = {}
        
        for column in data.select_dtypes(include=['float64', 'int64']).columns:
            if column == 'timestamp':
                continue
                
            vector = self.create_pattern_vector(data, column)
            if vector is None:
                continue
            
            # Search for similar patterns
            search_results = self.client.search(
                collection_name=f"{metric_type}_patterns",
                query_vector=vector.tolist(),
                limit=5
            )
            
            # If pattern is unique, mark as anomaly
            is_anomaly = len([
                r for r in search_results 
                if r.score > ANOMALY_CONFIG['similarity_threshold']
            ]) < 2
            
            anomalies[column] = is_anomaly
            
            # Store the pattern
            self.client.upsert(
                collection_name=f"{metric_type}_patterns",
                points=[models.PointStruct(
                    id=hash(f"{metric_type}_{column}_{len(vector)}"),
                    vector=vector.tolist(),
                    payload={
                        "metric_type": metric_type,
                        "metric_name": column,
                        "mean": float(np.mean(vector)),
                        "std": float(np.std(vector))
                    }
                )]
            )
        
        return anomalies