
def compute_statistics(df):
    stats = {}
    for col in df.select_dtypes(include=["int64","float64"]).columns:
        stats[col] = {
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "std": float(df[col].std())
        }
    return stats
