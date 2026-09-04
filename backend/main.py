import joblib
import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml.risk_explanation import get_risk_factors

# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ReturnGuard AI",
    description="Return Abuse Risk Scoring API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# LOAD TRAINED MODEL
# ============================================================

RISK_MODEL_PATH = r"E:\ReturnGuard-AI\models\return_risk_model.pkl"
ABUSE_MODEL_PATH = r"E:\ReturnGuard-AI\models\abuse_type_model.pkl"

risk_model = joblib.load(RISK_MODEL_PATH)
abuse_model = joblib.load(ABUSE_MODEL_PATH)

ABUSE_TYPES = {
    0: "Legitimate",
    1: "Policy Abuser",
    2: "Fraudulent Return",
    3: "Wardrobing"
}


# ============================================================
# INPUT DATA MODEL
# ============================================================

class ReturnRequest(BaseModel):

    age: int
    account_age_days: int

    customer_segment: str
    country: str
    platform: str
    device_type: str
    payment_method: str
    product_category: str

    avg_order_value_usd: float
    refund_amount_requested_usd: float

    is_high_value_item: int
    discount_used: int

    days_to_return: int
    return_reason: str

    total_orders_lifetime: int
    total_returns_lifetime: int
    return_rate_pct: float

    item_returned_opened: int
    return_packaging_intact: int
    photo_evidence_provided: int
    tracking_number_valid: int

    shipping_carrier: str

    address_change_before_delivery: int
    refund_to_different_account: int
    multiple_accounts_flag: int

    customer_support_contacts: int
    previous_dispute_count: int

    wishlist_to_cart_time_hrs: float


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "ReturnGuard AI API is running",
        "status": "success"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
def predict(request: ReturnRequest):

    # Convert request to DataFrame
    input_data = pd.DataFrame([request.model_dump()])

    # ========================================================
    # RISK MODEL
    # ========================================================

    risk_prediction = risk_model.predict(input_data)[0]

    risk_probability = risk_model.predict_proba(input_data)[0][1]

    risk_score = round(risk_probability * 100)


    # ========================================================
    # RISK LEVEL
    # ========================================================

    if risk_score < 30:
        risk_level = "LOW"

    elif risk_score < 70:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"


    # ========================================================
    # DECISION
    # ========================================================

    if risk_score < 30:
        decision = "AUTO_APPROVE"

    elif risk_score < 70:
        decision = "MANUAL_REVIEW"

    else:
        decision = "VERIFY_RETURN"


    # ========================================================
    # ABUSE TYPE MODEL
    # ========================================================

    abuse_prediction = abuse_model.predict(input_data)[0]

    abuse_type = ABUSE_TYPES[int(abuse_prediction)]


    # ========================================================
    # ABUSE TYPE PROBABILITIES
    # ========================================================

    abuse_probabilities = abuse_model.predict_proba(input_data)[0]

    abuse_confidence = abuse_probabilities[int(abuse_prediction)]


    # ========================================================
    # RESPONSE
    # ========================================================
    risk_factors = get_risk_factors(request.model_dump())
    return {
        "risk_score": risk_score,

        "risk_level": risk_level,

        "decision": decision,

        "prediction": (
            "RISKY"
            if risk_prediction == 1
            else "LEGITIMATE"
        ),

        "risk_probability": round(
            float(risk_probability),
            4
        ),

        "abuse_type": abuse_type,

        "abuse_confidence": round(
            float(abuse_confidence),
            4
        ),
        "risk_factors": risk_factors
    }