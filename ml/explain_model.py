import pandas as pd
import joblib


# ============================================================
# RETURNGUARD AI - MODEL EXPLANATION
# ============================================================

DATA_PATH = r"E:\ReturnGuard-AI\data\ecommerce_return_abuse_dataset.csv"
MODEL_PATH = r"E:\ReturnGuard-AI\models\return_risk_model.pkl"


print("=" * 60)
print("RETURNGUARD AI - MODEL EXPLANATION")
print("=" * 60)


# ============================================================
# 1. LOAD DATA AND MODEL
# ============================================================

df = pd.read_csv(DATA_PATH)

model = joblib.load(MODEL_PATH)


# ============================================================
# 2. REMOVE NON-MODEL COLUMNS
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


# ============================================================
# 3. GET PREPROCESSOR AND CLASSIFIER
# ============================================================

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]


# ============================================================
# 4. TRANSFORM FEATURES
# ============================================================

X_transformed = preprocessor.transform(X)


# ============================================================
# 5. GET FEATURE NAMES
# ============================================================

feature_names = preprocessor.get_feature_names_out()


# ============================================================
# 6. GET MODEL COEFFICIENTS
# ============================================================

coefficients = classifier.coef_[0]


# ============================================================
# 7. FEATURE IMPORTANCE BY ABSOLUTE COEFFICIENT
# ============================================================

importance_df = pd.DataFrame({
    "feature": feature_names,
    "coefficient": coefficients,
    "importance": abs(coefficients)
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)


print("\nTOP 20 MODEL FEATURES")
print("=" * 60)

print(
    importance_df.head(20).to_string(index=False)
)


# ============================================================
# 8. POSITIVE RISK FEATURES
# ============================================================

positive_features = importance_df[
    importance_df["coefficient"] > 0
].sort_values(
    by="coefficient",
    ascending=False
)


print("\nTOP FEATURES INCREASING RISK")
print("=" * 60)

print(
    positive_features.head(15).to_string(index=False)
)


# ============================================================
# 9. NEGATIVE RISK FEATURES
# ============================================================

negative_features = importance_df[
    importance_df["coefficient"] < 0
].sort_values(
    by="coefficient",
    ascending=True
)


print("\nTOP FEATURES DECREASING RISK")
print("=" * 60)

print(
    negative_features.head(15).to_string(index=False)
)


print("\nExplanation analysis completed!")