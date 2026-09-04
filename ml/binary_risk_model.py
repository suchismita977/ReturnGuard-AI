import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("RETURNGUARD AI - BINARY RISK MODEL")
print("=" * 60)

print("\nOriginal dataset:", df.shape)


# ============================================================
# 2. CREATE BINARY RISK TARGET
# ============================================================
#
# 0 = Legitimate
# 1 = Any type of return abuse
#
# Original labels:
# 0 = Legitimate
# 1 = Policy Abuser
# 2 = Fraudulent Return
# 3 = Wardrobing
# ============================================================

df["risk_label"] = (df["abuse_label"] != 0).astype(int)

print("\nRisk distribution:")
print(df["risk_label"].value_counts())

print("\nRisk percentages:")
print(
    (df["risk_label"].value_counts(normalize=True) * 100)
    .round(2)
)


# ============================================================
# 3. REMOVE IDENTIFIERS / TARGET / POST-RETURN INFORMATION
# ============================================================

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


# ============================================================
# 4. IDENTIFY FEATURE TYPES
# ============================================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nNumerical features:", len(numerical_features))
print("Categorical features:", len(categorical_features))


# ============================================================
# 5. PREPROCESSING
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
# 6. MODEL
# ============================================================

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


# ============================================================
# 7. TRAIN / TEST SPLIT
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
# 8. TRAIN MODEL
# ============================================================

print("\nTraining binary risk model...")

model.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# 9. PREDICTION
# ============================================================

y_pred = model.predict(X_test)

# Probability of risky class
y_probability = model.predict_proba(X_test)[:, 1]


# ============================================================
# 10. EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:")
print(round(accuracy_score(y_test, y_pred), 4))

print("\nPrecision:")
print(round(precision_score(y_test, y_pred), 4))

print("\nRecall:")
print(round(recall_score(y_test, y_pred), 4))

print("\nF1 Score:")
print(round(f1_score(y_test, y_pred), 4))


# ============================================================
# 11. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Risky"
        ]
    )
)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

print("\nConfusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)


# ============================================================
# 13. FALSE POSITIVE RATE
# ============================================================

tn, fp, fn, tp = cm.ravel()

false_positive_rate = fp / (fp + tn)

print("\nFalse Positive Rate:")
print(round(false_positive_rate, 4))


# ============================================================
# 14. EXAMPLE RISK SCORES
# ============================================================

print("\nExample Risk Probabilities:")

for probability in y_probability[:10]:

    risk_score = round(probability * 100)

    print(
        f"Probability: {probability:.4f}"
        f"  →  Risk Score: {risk_score}/100"
    )