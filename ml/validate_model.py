import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

# ============================================================
# 2. REMOVE IDs / TARGET / POSSIBLE POST-RETURN LEAKAGE
# ============================================================

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

# ============================================================
# 3. IDENTIFY FEATURES
# ============================================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

# ============================================================
# 4. PREPROCESSING
# ============================================================

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

# ============================================================
# 5. MODEL
# ============================================================

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

# ============================================================
# 6. 5-FOLD CROSS VALIDATION
# ============================================================

print("=" * 60)
print("RETURNGUARD AI - CROSS VALIDATION")
print("=" * 60)

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="f1_macro",
    n_jobs=-1
)

print("\nF1 Macro scores:")
for i, score in enumerate(scores, start=1):
    print(f"Fold {i}: {score:.4f}")

print("\nMean F1 Macro:", round(scores.mean(), 4))
print("Standard Deviation:", round(scores.std(), 4))