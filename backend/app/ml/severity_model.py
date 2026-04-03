import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import os
from .data_generator import generate_mock_historical_data

MODEL_PATH = "rf_severity_model.pkl"
XGB_MODEL_PATH = "xgb_severity_model.json"
ENCODER_PATH = "label_encoders.pkl"

def train_models():
    # Attempt to load data, if not exist, generate
    if not os.path.exists("historical_accidents.csv"):
        df = generate_mock_historical_data()
        df.to_csv("historical_accidents.csv", index=False)
    else:
        df = pd.read_csv("historical_accidents.csv")
        
    # Preprocessing
    features = ['time_of_day', 'weather', 'traffic_index', 'road_type']
    X = df[features]
    y = df['severity']
    
    # Encode categorical variables
    encoders = {}
    for col in ['weather', 'road_type']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
        
    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(y)
    encoders['severity'] = le_y
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Train XGBoost
    xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    xgb_model.fit(X_train, y_train)
    
    # Save models and encoders
    joblib.dump(rf_model, MODEL_PATH)
    xgb_model.save_model(XGB_MODEL_PATH)
    joblib.dump(encoders, ENCODER_PATH)
    
    print("Models trained and saved successfully.")
    
    # Print accuracy at training time as well
    print_model_accuracy(X_test, y_test, rf_model, xgb_model)

def print_model_accuracy(X_test=None, y_test=None, rf_model=None, xgb_model=None):
    """
    Prints the accuracy of the models. If provided with current test data, uses it.
    Otherwise, loads the saved models and calculates the score isolated on a partitioned test set.
    """
    if X_test is None:
        if not os.path.exists("historical_accidents.csv") or not os.path.exists(MODEL_PATH):
            return
            
        df = pd.read_csv("historical_accidents.csv")
        features = ['time_of_day', 'weather', 'traffic_index', 'road_type']
        X = df[features].copy()
        y = df['severity']
        
        try:
            encoders = joblib.load(ENCODER_PATH)
            for col in ['weather', 'road_type']:
                X[col] = encoders[col].transform(X[col])
            y_encoded = encoders['severity'].transform(y)
            
            # Formally partition to ensure we don't evaluate on trained data
            _, X_test, _, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
            
            rf_model = joblib.load(MODEL_PATH)
            xgb_model = xgb.XGBClassifier()
            xgb_model.load_model(XGB_MODEL_PATH)
        except Exception:
            return

    try:
        rf_pred = rf_model.predict(X_test)
        xgb_pred = xgb_model.predict(X_test)
        
        rf_acc = accuracy_score(y_test, rf_pred) * 100
        xgb_acc = accuracy_score(y_test, xgb_pred) * 100
        
        # Calculate Precision, Recall, F1 (weighted average for multi-class)
        rf_prec, rf_rec, rf_f1, _ = precision_recall_fscore_support(y_test, rf_pred, average='weighted', zero_division=0)
        xgb_prec, xgb_rec, xgb_f1, _ = precision_recall_fscore_support(y_test, xgb_pred, average='weighted', zero_division=0)
        
        print("\n" + "="*60)
        print("🚦 AI MODEL METRICS REPORT (FOR PROJECT GUIDE) 🚦")
        print("="*60)
        print(f" [ Random Forest Classifier ]")
        print(f"   Accuracy  : {rf_acc:.2f}%")
        print(f"   Precision : {rf_prec:.4f}")
        print(f"   Recall    : {rf_rec:.4f}")
        print(f"   F1 Score  : {rf_f1:.4f}")
        print("-" * 60)
        print(f" [ XGBoost Classifier ]")
        print(f"   Accuracy  : {xgb_acc:.2f}%")
        print(f"   Precision : {xgb_prec:.4f}")
        print(f"   Recall    : {xgb_rec:.4f}")
        print(f"   F1 Score  : {xgb_f1:.4f}")
        print("="*60 + "\n")
    except Exception as e:
        print(f"Could not calculate accuracy: {e}")

def predict_severity(time_of_day, weather, traffic_index, road_type, use_xgboost=True):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        train_models()
        
    encoders = joblib.load(ENCODER_PATH)
    
    # Prepare input
    # Assuming valid inputs for categorical data matching the mock generators.
    # Fallback to 0 if unknown category.
    try:
        weather_encoded = encoders['weather'].transform([weather])[0]
    except:
        weather_encoded = 0
        
    try:
        road_type_encoded = encoders['road_type'].transform([road_type])[0]
    except:
        road_type_encoded = 0
        
    input_features = np.array([[time_of_day, weather_encoded, traffic_index, road_type_encoded]])
    
    if use_xgboost:
        model = xgb.XGBClassifier()
        model.load_model(XGB_MODEL_PATH)
        pred_encoded = model.predict(input_features)[0]
    else:
        model = joblib.load(MODEL_PATH)
        pred_encoded = model.predict(input_features)[0]
        
    severity = encoders['severity'].inverse_transform([pred_encoded])[0]
    return severity

if __name__ == "__main__":
    train_models()
