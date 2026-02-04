
def generate_insights(stats, df):
    lines = []
    for col, v in stats.items():
        lines.append(f"{col}: Mean={v['mean']:.2f}, Min={v['min']}, Max={v['max']}")
    anomalies = (df["Anomaly"] == -1).sum()
    lines.append(f"Total anomalies detected: {anomalies}")
    return "\n".join(lines)
