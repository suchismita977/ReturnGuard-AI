import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

# Remove identifiers, target and post-return information
columns_to_drop = [
    "order_id",
    "customer_id",
    "order_date",
    "return_date",
    "review_left_after_return",
    "abuse_type",
    "abuse_label"
]

X = df.drop(columns=columns_to_drop)
y = df["abuse_label"]

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

preprocessor = ColumnTransformer([
    (
        "cat",
        OneHotEncoder(handle_unknown="ignore"),
        categorical_features
    )
], remainder="passthrough")

model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )
    )
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Random Forest...")
model.fit(X_train, y_train)

print("Training completed!")

# Get transformed feature names
feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

importances = model.named_steps[
    "classifier"
].feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nTOP 20 FEATURES")
print("=" * 60)

print(
    importance_df.head(20).to_string(index=False)
)