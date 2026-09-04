import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

# Create binary target
df["risk_label"] = (df["abuse_label"] != 0).astype(int)

# Remove identifiers and leakage
columns_to_drop = [
    "order_id",
    "customer_id",
    "order_date",
    "return_date",
    "review_left_after_return",
    "abuse_type",
    "abuse_label",
    "risk_label"
]

X = df.drop(columns=columns_to_drop)
y = df["risk_label"]

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numerical_features),
    ("cat", categorical_pipeline, categorical_features)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)[:, 1]

print("=" * 60)
print("RISK PROBABILITY ANALYSIS")
print("=" * 60)

print("\nMinimum probability:", round(probabilities.min(), 6))
print("Maximum probability:", round(probabilities.max(), 6))
print("Mean probability:", round(probabilities.mean(), 6))

print("\nPercentiles:")

for percentile in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
    value = pd.Series(probabilities).quantile(percentile / 100)
    print(f"{percentile}th percentile: {value:.6f}")

# Probability buckets
bins = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]

labels = [
    "0-10%",
    "10-30%",
    "30-50%",
    "50-70%",
    "70-90%",
    "90-100%"
]

probability_groups = pd.cut(
    probabilities,
    bins=bins,
    labels=labels,
    include_lowest=True
)

print("\nProbability Distribution:")

print(
    probability_groups.value_counts()
    .sort_index()
)