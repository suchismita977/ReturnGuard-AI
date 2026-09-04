import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression


# ============================================================
# RETURNGUARD AI - CALIBRATED RISK MODEL
# ============================================================

print("=" * 60)
print("RETURNGUARD AI - CALIBRATED RISK MODEL")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:", df.shape)


# ============================================================
# 2. CREATE BINARY TARGET
# ============================================================

# 0 = Legitimate
# 1 = Risky
#
# Policy Abuser, Fraudulent Return and Wardrobing
# are considered risky.

df["risk_label"] = (df["abuse_label"] != 0).astype(int)


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
# 4. FEATURE TYPES
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
# 6. BASE LOGISTIC REGRESSION
# ============================================================

base_model = Pipeline([
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
# 7. TRAIN / CALIBRATION SPLIT
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
# 8. TRAIN BASE MODEL
# ============================================================

print("\nTraining base model...")

base_model.fit(X_train, y_train)

print("Base model trained!")


# ============================================================
# 9. CALIBRATE PROBABILITIES
# ============================================================

print("\nCalibrating probabilities...")

calibrated_model = CalibratedClassifierCV(
    base_model,
    method="sigmoid",
    cv=5
)

calibrated_model.fit(X_train, y_train)

print("Calibration completed!")


# ============================================================
# 10. CHECK PROBABILITY DISTRIBUTION
# ============================================================

probabilities = calibrated_model.predict_proba(X_test)[:, 1]

print("\nCalibrated probability statistics:")

print("Minimum:", round(probabilities.min(), 4))
print("Maximum:", round(probabilities.max(), 4))
print("Mean:", round(probabilities.mean(), 4))

print("\nPercentiles:")

for percentile in [1, 5, 10, 25, 50, 75, 90, 95, 99]:

    value = pd.Series(probabilities).quantile(percentile / 100)

    print(
        f"{percentile}th percentile:",
        round(value, 4)
    )


# ============================================================
# 11. SAVE MODEL
# ============================================================

MODEL_PATH = r"E:\ReturnGuard-AI\models\calibrated_risk_model.pkl"

joblib.dump(calibrated_model, MODEL_PATH)

print("\n" + "=" * 60)
print("CALIBRATED MODEL SAVED")
print("=" * 60)

print(MODEL_PATH)