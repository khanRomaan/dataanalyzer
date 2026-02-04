
def profile_data(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Numeric Columns": df.select_dtypes(include=["int64","float64"]).columns.tolist(),
        "Categorical Columns": df.select_dtypes(include=["object"]).columns.tolist(),
        "Missing Values": df.isnull().sum().to_dict()
    }
