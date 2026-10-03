import joblib
import os

def predict_overflow_risk(features):
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError("ML model not found. Please run seed script first.")
    
    clf = joblib.load(model_path)
    
    prob = clf.predict_proba([features])[0][1] 
    
    risk_score = prob * 100
    
    if risk_score <= 30:
        level = "LOW"
    elif risk_score <= 60:
        level = "MEDIUM"
    elif risk_score <= 80:
        level = "HIGH"
    else:
        level = "CRITICAL"
        
    return float(round(prob, 2)), level
