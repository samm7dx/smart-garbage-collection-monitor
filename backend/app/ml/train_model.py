import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train():
    print("Training ML model...")
    np.random.seed(42)
    n_samples = 500

    fill_percentage = np.random.uniform(0, 100, n_samples)
    fill_growth_per_day = np.random.uniform(0, 30, n_samples)
    average_delay_minutes = np.random.uniform(0, 300, n_samples)
    missed_collections = np.random.randint(0, 4, n_samples)
    complaints = np.random.randint(0, 5, n_samples)
    frequency = np.random.randint(1, 8, n_samples)

    X = np.column_stack((
        fill_percentage,
        fill_growth_per_day,
        average_delay_minutes,
        missed_collections,
        complaints,
        frequency
    ))

    y = np.zeros(n_samples)
    for i in range(n_samples):
        score = (fill_percentage[i] * 0.4 + 
                 fill_growth_per_day[i] * 1.5 + 
                 average_delay_minutes[i] * 0.1 + 
                 missed_collections[i] * 15 + 
                 complaints[i] * 10)
        if score > 70:
            y[i] = 1

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)

    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train()
