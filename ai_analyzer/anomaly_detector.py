
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, numeric_cols):
    if not numeric_cols:
        df["Anomaly"] = 0
        return df

    model = IsolationForest(contamination=0.05, random_state=42)
    df["Anomaly"] = model.fit_predict(df[numeric_cols])
    return df
