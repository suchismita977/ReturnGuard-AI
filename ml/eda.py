import pandas as pd

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RETURNGUARD AI - DATASET ANALYSIS")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nAbuse Type Distribution:")
print(df["abuse_type"].value_counts())

print("\nAbuse Label Distribution:")
print(df["abuse_label"].value_counts())

print("\nNumerical Summary:")
print(df.describe())