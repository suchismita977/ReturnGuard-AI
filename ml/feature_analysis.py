import pandas as pd

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RETURNGUARD AI - FEATURE ANALYSIS")
print("=" * 60)

# Target distribution
print("\nTarget Distribution:")
print(df["abuse_label"].value_counts(normalize=True).sort_index())

# Average numerical features by abuse class
print("\nNumerical Features by Abuse Class:")
print(
    df.groupby("abuse_label")
      .mean(numeric_only=True)
      .round(2)
      .to_string()
)

# Categorical features
categorical_columns = df.select_dtypes(include=["object"]).columns

print("\nCategorical Columns:")
for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].value_counts().head(10))