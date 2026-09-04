# 🛡️ ReturnGuard AI

### Intelligent E-commerce Return Risk & Abuse Detection

ReturnGuard AI is an AI-powered return investigation and risk assessment system designed to help e-commerce merchants identify potentially abusive or fraudulent return requests before processing them.

The system analyzes **28 return-related signals**, generates a risk score, classifies the likely abuse pattern, and provides an actionable recommendation for the merchant.

---

## 🚨 Problem

E-commerce returns can create significant losses when return policies are repeatedly abused or when fraudulent return claims are submitted.

Traditional rule-based systems often rely on individual conditions such as return frequency or refund amount.

However, return abuse can involve multiple interacting signals.

ReturnGuard AI addresses this problem by combining customer, order, return, verification, and historical risk signals into a structured AI-assisted investigation workflow.

---

## 💡 Solution

ReturnGuard AI evaluates a return request using **28 signals across five investigation stages**:

1. Customer Profile
2. Order Details
3. Return Behavior
4. Verification
5. Risk Signals

The signals are processed by machine-learning models to produce:

- Risk score
- Risk level
- Risk prediction
- Likely abuse type
- Abuse confidence
- Recommended merchant action
- Key risk factors

---

## 🔄 How It Works

```text
Merchant
   │
   ▼
React Frontend
   │
   │ 28 Return Signals
   ▼
FastAPI Backend
   │
   ▼
Data Validation & Preprocessing
   │
   ├───────────────┐
   ▼               ▼
Risk Model      Abuse Model
   │               │
   ▼               ▼
Risk Score     Abuse Type
   │               │
   └───────┬───────┘
           ▼
      Decision Layer
           │
           ▼
    Result Dashboard

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Frontend** | React, Vite, JavaScript, CSS |
| **Backend** | Python, FastAPI, Pydantic |
| **Machine Learning** | Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Model Storage** | Pickle (`.pkl`) |
| **Data Format** | CSV |
| **Analysis** | Jupyter Notebook |
| **Communication** | REST API, JSON over HTTP |
| **Version Control** | Git, GitHub |

---

Intelligent E-commerce Return Risk & Abuse Detection

An AI-assisted system for identifying potentially risky e-commerce returns and supporting merchant decision-making.
