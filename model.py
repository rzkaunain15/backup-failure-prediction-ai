import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class BackupFailurePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = ['duration_mins', 'latency_ms', 'storage_usage_pct', 'server_load_pct']

    def preprocess_data(self, df):
        """Prepare features and target for training/prediction."""
        X = df[self.features]
        # Status format from simulation: "Success" or "Failed"
        if 'status' in df.columns:
            y = (df['status'] == 'Failed').astype(int)
            return X, y
        return X

    def train(self, historical_df):
        """Train the model on historical Veeam log data."""
        X, y = self.preprocess_data(historical_df)
        
        # Split data just to log some metrics during training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"[*] Model trained successfully. Validation Accuracy: {accuracy * 100:.2f}%")

    def predict(self, job_data):
        """
        Predict failure probability for a single incoming job or batch.
        job_data should be a dictionary or DataFrame.
        Returns: probability of failure, risk level.
        """
        if isinstance(job_data, dict):
            df = pd.DataFrame([job_data])
        else:
            df = job_data
            
        X = self.preprocess_data(df)
        
        # predict_proba returns [prob_class_0, prob_class_1]
        probs = self.model.predict_proba(X)
        
        results = []
        for prob in probs:
            fail_prob = prob[1]
            if fail_prob > 0.75:
                risk_level = "HIGH"
            elif fail_prob > 0.40:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"
                
            results.append((fail_prob, risk_level))
            
        return results if len(results) > 1 else results[0]
