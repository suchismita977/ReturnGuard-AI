import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

# ============================================================
# CREATE BINARY TARGET
# ============================================================

df["risk_label"] = (df["abuse_label"] != 0).astype(int)

# ============================================================
# COLUMNS THAT SHOULD NEVER BE FEATURES
# ============================================================

base_drop = [
    "order_id",
    "customer_id",
    "order_date",
    "return_date",
    "review_left_after_return",
    "abuse_type",
    "abuse_label",
    "risk_label"
]

# ============================================================
# FEATURES TO TEST
# ============================================================

features_to_remove = [
    [],
    ["days_to_return"],
    ["return_rate_pct"],
    ["wishlist_to_cart_time_hrs"],
    ["days_to_return", "return_rate_pct"],
    [
        "days_to_return",
        "return_rate_pct",
        "wishlist_to_cart_time_hrs"
    ]
]

# ============================================================
# RUN EXPERIMENT
# ============================================================

print("=" * 70)
print("RETURNGUARD AI - FEATURE ABLATION TEST")
print("=" * 70)

for removed_features in features_to_remove:

    drop_columns = base_drop + removed_features

    X = df.drop(columns=drop_columns)
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
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
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

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    score = f1_score(y_test, y_pred)

    if removed_features:
        removed_text = ", ".join(removed_features)
    else:
        removed_text = "None"

    print(
        f"\nRemoved: {removed_text}"
    )

    print(
        f"F1 Score: {score:.4f}"
    )