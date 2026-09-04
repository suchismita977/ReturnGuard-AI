import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RETURNGUARD AI - MODEL TRAINING")
print("=" * 60)

print("\nDataset shape:", df.shape)


# ============================================================
# 2. REMOVE COLUMNS WE SHOULD NOT USE
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

print("\nFeatures used:", X.shape[1])
print("Target classes:", sorted(y.unique()))


# ============================================================
# 3. IDENTIFY NUMERICAL & CATEGORICAL FEATURES
# ============================================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nNumerical features:")
print(numerical_features)

print("\nCategorical features:")
print(categorical_features)


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
# 5. CREATE MODEL PIPELINE
# ============================================================

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ============================================================
# 7. TRAIN MODEL
# ============================================================

print("\nTraining Logistic Regression...")

model.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# 8. PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 9. EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:")
print(round(accuracy_score(y_test, y_pred), 4))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Policy Abuser",
            "Fraudulent Return",
            "Wardrobing"
        ]
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))