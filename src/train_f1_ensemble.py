import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.ensemble import VotingClassifier
import joblib
import os

# Ensemble models
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

def preprocess(df, categorical_cols, drop_cols, target_col):
    df = df.copy()
    # Fill missing values
    df = df.fillna(-1)
    # Only use categorical columns that exist
    categorical_cols = [col for col in categorical_cols if col in df.columns]
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    # Only drop columns that exist
    drop_cols = [col for col in drop_cols if col in df.columns]
    X = df.drop(drop_cols + [target_col], axis=1)
    y = df[target_col]
    return X, y, encoders

def train_and_evaluate(X, y, model_name, save_path):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    # Define models
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    lgb = LGBMClassifier(random_state=42)
    cat = CatBoostClassifier(verbose=0, random_state=42)
    ensemble = VotingClassifier(estimators=[
        ('xgb', xgb),
        ('lgb', lgb),
        ('cat', cat)
    ], voting='soft')
    # Train
    ensemble.fit(X_train, y_train)
    # Predict
    y_pred = ensemble.predict(X_test)
    y_proba = ensemble.predict_proba(X_test)[:,1]
    # Metrics
    print(f"\n=== {model_name} ===")
    print(classification_report(y_test, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
    # Save model
    joblib.dump(ensemble, save_path)
    print(f"Model saved to {save_path}")
    return ensemble

def main():
    df = pd.read_csv('data/merged/f1_model_data.csv')
    # Features to encode (removed 'Compound')
    categorical_cols = [
        'Abbreviation', 'TeamName', 'Country', 'RaceName', 'driver_team_combo', 'CountryCode'
    ]
    # Drop columns not useful for modeling (removed 'Compound')
    drop_cols = [
        'FullName', 'FirstName', 'LastName', 'HeadshotUrl', 'TeamColor', 'TeamId', 'DriverId',
        'Time', 'Status', 'RaceName', 'Country', 'driver_team_combo', 'Year', 'Round', 'BroadcastName',
        'Q1', 'Q2', 'Q3', 'LapStartDate', 'LapStartTime', 'PitOutTime', 'PitInTime', 'DeletedReason',
        'FastF1Generated', 'IsAccurate', 'Deleted', 'TrackStatus', 'LapNumber', 'Stint', 'LapTime',
        'Sector1Time', 'Sector2Time', 'Sector3Time', 'Sector1SessionTime', 'Sector2SessionTime',
        'Sector3SessionTime', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'LapStartTime', 'LapStartDate',
        'RaceName', 'Country', 'DriverNumber', 'Driver', 'DriverId', 'TeamId', 'TeamColor', 'HeadshotUrl',
        'FullName', 'FirstName', 'LastName', 'Abbreviation', 'driver_team_combo', 'CountryCode'
    ]
    # Winner prediction
    X_win, y_win, enc_win = preprocess(df, categorical_cols, drop_cols, 'is_winner')
    train_and_evaluate(X_win, y_win, 'Winner Prediction', 'models/ensemble_winner.joblib')
    # Podium prediction
    X_pod, y_pod, enc_pod = preprocess(df, categorical_cols, drop_cols, 'podium')
    train_and_evaluate(X_pod, y_pod, 'Podium Prediction', 'models/ensemble_podium.joblib')
    # Save encoders
    os.makedirs('models', exist_ok=True)
    joblib.dump(enc_win, 'models/encoders_winner.joblib')
    joblib.dump(enc_pod, 'models/encoders_podium.joblib')
    print("Encoders saved.")

if __name__ == "__main__":
    main() 