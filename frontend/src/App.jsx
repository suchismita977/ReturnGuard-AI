import { useEffect, useMemo, useState } from "react";
import "./App.css";

/* =========================================================
   INITIAL FORM — ALL 28 MODEL INPUTS
========================================================= */

const initialForm = {
  age: "",
  account_age_days: "",
  customer_segment: "Regular",
  country: "US",
  platform: "Web",
  device_type: "Desktop",

  avg_order_value_usd: "",
  refund_amount_requested_usd: "",
  product_category: "Electronics",
  payment_method: "Credit Card",
  is_high_value_item: "0",
  discount_used: "0",

  days_to_return: "",
  return_reason: "Changed Mind",
  total_orders_lifetime: "",
  total_returns_lifetime: "",
  return_rate_pct: "",
  wishlist_to_cart_time_hrs: "",

  item_returned_opened: "0",
  return_packaging_intact: "1",
  photo_evidence_provided: "1",
  tracking_number_valid: "1",
  shipping_carrier: "UPS",

  previous_dispute_count: "",
  customer_support_contacts: "",
  multiple_accounts_flag: "0",
  refund_to_different_account: "0",
  address_change_before_delivery: "0",
};

/* =========================================================
   DROPDOWN OPTIONS
========================================================= */

const options = {
  customer_segment: ["New", "Regular", "Loyal", "VIP"],

  country: [
    "US",
    "UK",
    "Canada",
    "India",
    "Australia",
    "Germany",
  ],

  platform: ["Web", "Mobile App"],

  device_type: [
    "Desktop",
    "Mobile",
    "Tablet",
    "iPad",
  ],

  product_category: [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Toys",
  ],

  payment_method: [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "UPI",
    "Bank Transfer",
  ],

  return_reason: [
    "Changed Mind",
    "Defective/Broken",
    "Wrong Item Sent",
    "Quality Issue",
    "Size/Fit Issue",
    "Not as Described",
    "Other",
  ],

  shipping_carrier: [
    "UPS",
    "FedEx",
    "USPS",
    "DHL",
    "Other",
  ],
};

/* =========================================================
   5 WORKFLOW STEPS
========================================================= */

const steps = [
  {
    number: "01",
    short: "Customer",
    title: "Customer Profile",
    description:
      "Identity, account history and customer context.",
    fields: [
      "age",
      "account_age_days",
      "customer_segment",
      "country",
      "platform",
      "device_type",
    ],
  },

  {
    number: "02",
    short: "Order",
    title: "Order Details",
    description:
      "Transaction value, product and payment information.",
    fields: [
      "avg_order_value_usd",
      "refund_amount_requested_usd",
      "product_category",
      "payment_method",
      "is_high_value_item",
      "discount_used",
    ],
  },

  {
    number: "03",
    short: "Return",
    title: "Return Behavior",
    description:
      "Historical and current return patterns.",
    fields: [
      "days_to_return",
      "return_reason",
      "total_orders_lifetime",
      "total_returns_lifetime",
      "return_rate_pct",
      "wishlist_to_cart_time_hrs",
    ],
  },

  {
    number: "04",
    short: "Verification",
    title: "Return Verification",
    description:
      "Evidence and fulfillment verification signals.",
    fields: [
      "item_returned_opened",
      "return_packaging_intact",
      "photo_evidence_provided",
      "tracking_number_valid",
      "shipping_carrier",
    ],
  },

  {
    number: "05",
    short: "Risk",
    title: "Risk Signals",
    description:
      "Disputes, account anomalies and refund indicators.",
    fields: [
      "previous_dispute_count",
      "customer_support_contacts",
      "multiple_accounts_flag",
      "refund_to_different_account",
      "address_change_before_delivery",
    ],
  },
];

/* =========================================================
   FIELD METADATA
========================================================= */

const fieldMeta = {
  age: {
    label: "Customer Age",
    type: "number",
    placeholder: "e.g. 29",
  },

  account_age_days: {
    label: "Account Age",
    type: "number",
    placeholder: "Days",
  },

  customer_segment: {
    label: "Customer Segment",
    type: "select",
    options: options.customer_segment,
  },

  country: {
    label: "Country",
    type: "select",
    options: options.country,
  },

  platform: {
    label: "Platform",
    type: "select",
    options: options.platform,
  },

  device_type: {
    label: "Device Type",
    type: "select",
    options: options.device_type,
  },

  avg_order_value_usd: {
    label: "Average Order Value",
    type: "number",
    placeholder: "USD",
    step: "0.01",
  },

  refund_amount_requested_usd: {
    label: "Refund Amount Requested",
    type: "number",
    placeholder: "USD",
    step: "0.01",
  },

  product_category: {
    label: "Product Category",
    type: "select",
    options: options.product_category,
  },

  payment_method: {
    label: "Payment Method",
    type: "select",
    options: options.payment_method,
  },

  is_high_value_item: {
    label: "High-Value Item",
    type: "binary",
  },

  discount_used: {
    label: "Discount Used",
    type: "binary",
  },

  days_to_return: {
    label: "Days to Return",
    type: "number",
    placeholder: "Days",
  },

  return_reason: {
    label: "Return Reason",
    type: "select",
    options: options.return_reason,
  },

  total_orders_lifetime: {
    label: "Total Orders",
    type: "number",
    placeholder: "Lifetime orders",
  },

  total_returns_lifetime: {
    label: "Total Returns",
    type: "number",
    placeholder: "Lifetime returns",
  },

  return_rate_pct: {
    label: "Return Rate",
    type: "number",
    placeholder: "%",
    step: "0.01",
  },

  wishlist_to_cart_time_hrs: {
    label: "Wishlist → Cart Time",
    type: "number",
    placeholder: "Hours",
    step: "0.01",
  },

  item_returned_opened: {
    label: "Item Returned Opened",
    type: "binary",
  },

  return_packaging_intact: {
    label: "Packaging Intact",
    type: "binary",
  },

  photo_evidence_provided: {
    label: "Photo Evidence Provided",
    type: "binary",
  },

  tracking_number_valid: {
    label: "Tracking Number Valid",
    type: "binary",
  },

  shipping_carrier: {
    label: "Shipping Carrier",
    type: "select",
    options: options.shipping_carrier,
  },

  previous_dispute_count: {
    label: "Previous Disputes",
    type: "number",
    placeholder: "Count",
  },

  customer_support_contacts: {
    label: "Support Contacts",
    type: "number",
    placeholder: "Count",
  },

  multiple_accounts_flag: {
    label: "Multiple Accounts",
    type: "binary",
  },

  refund_to_different_account: {
    label: "Refund to Different Account",
    type: "binary",
  },

  address_change_before_delivery: {
    label: "Address Changed Before Delivery",
    type: "binary",
  },
};

/* =========================================================
   NUMERIC FIELDS
========================================================= */

const numericFields = [
  "age",
  "account_age_days",
  "avg_order_value_usd",
  "refund_amount_requested_usd",
  "is_high_value_item",
  "discount_used",
  "days_to_return",
  "total_orders_lifetime",
  "total_returns_lifetime",
  "return_rate_pct",
  "wishlist_to_cart_time_hrs",
  "item_returned_opened",
  "return_packaging_intact",
  "photo_evidence_provided",
  "tracking_number_valid",
  "previous_dispute_count",
  "customer_support_contacts",
  "multiple_accounts_flag",
  "refund_to_different_account",
  "address_change_before_delivery",
];

/* =========================================================
   ANALYSIS ANIMATION
========================================================= */

const analysisStages = [
  "Collecting signals",
  "Evaluating return behavior",
  "Running risk model",
  "Classifying abuse pattern",
  "Generating recommendation",
];

/* =========================================================
   FIELD COMPONENT
========================================================= */

function Field({ field, value, onChange }) {
  const meta = fieldMeta[field];

  if (!meta) return null;

  return (
    <div className="field">
      <label htmlFor={field}>
        {meta.label}
        <span className="field-key">{field}</span>
      </label>

      {meta.type === "select" && (
        <select
          id={field}
          value={value}
          onChange={(e) =>
            onChange(field, e.target.value)
          }
        >
          {meta.options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      )}

      {meta.type === "number" && (
        <input
          id={field}
          type="number"
          value={value}
          placeholder={meta.placeholder}
          step={meta.step || "1"}
          min="0"
          onChange={(e) =>
            onChange(field, e.target.value)
          }
        />
      )}

      {meta.type === "binary" && (
        <select
          id={field}
          value={value}
          onChange={(e) =>
            onChange(field, e.target.value)
          }
        >
          <option value="0">No</option>
          <option value="1">Yes</option>
        </select>
      )}
    </div>
  );
}

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [formData, setFormData] =
    useState(initialForm);

  const [currentStep, setCurrentStep] =
    useState(0);

  const [reviewing, setReviewing] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [analysisStage, setAnalysisStage] =
    useState(-1);

  /* =======================================================
     VISITED STEPS

     This prevents every step from showing ✓ initially.
  ======================================================= */

  const [visitedSteps, setVisitedSteps] =
    useState(() => {
      try {
        const saved = localStorage.getItem(
          "returnguard-visited-steps"
        );

        return saved
          ? JSON.parse(saved)
          : [false, false, false, false, false];
      } catch {
        return [false, false, false, false, false];
      }
    });

  /* =======================================================
     DARK MODE
  ======================================================= */

  const [darkMode, setDarkMode] =
    useState(() => {
      return (
        localStorage.getItem(
          "returnguard-theme"
        ) === "dark"
      );
    });

  /* =======================================================
     INVESTIGATION ID
  ======================================================= */

  const [investigationId] =
    useState(() => {
      const year =
        new Date().getFullYear();

      const random =
        Math.floor(
          1000 + Math.random() * 9000
        );

      return `RG-${year}-${random}`;
    });

  /* =======================================================
     RESTORE SAVED DRAFT
  ======================================================= */

  useEffect(() => {
    const savedDraft =
      localStorage.getItem(
        "returnguard-draft"
      );

    if (savedDraft) {
      try {
        const parsed =
          JSON.parse(savedDraft);

        setFormData({
          ...initialForm,
          ...parsed,
        });
      } catch {
        console.log(
          "Unable to restore draft."
        );
      }
    }
  }, []);

  /* =======================================================
     AUTO SAVE
  ======================================================= */

  useEffect(() => {
    localStorage.setItem(
      "returnguard-draft",
      JSON.stringify(formData)
    );
  }, [formData]);

  /* =======================================================
     SAVE VISITED STEPS
  ======================================================= */

  useEffect(() => {
    localStorage.setItem(
      "returnguard-visited-steps",
      JSON.stringify(visitedSteps)
    );
  }, [visitedSteps]);

  /* =======================================================
     DARK MODE EFFECT
  ======================================================= */

  useEffect(() => {
    document.body.classList.toggle(
      "dark-mode",
      darkMode
    );

    localStorage.setItem(
      "returnguard-theme",
      darkMode ? "dark" : "light"
    );
  }, [darkMode]);

  /* =======================================================
     COMPLETED STEP CALCULATION
  ======================================================= */

  const completedSteps = useMemo(() => {
    return steps.map(
      (step, index) => {
        if (!visitedSteps[index]) {
          return false;
        }

        return step.fields.every(
          (field) =>
            formData[field] !==
              undefined &&
            formData[field] !== null &&
            String(formData[field]).trim() !== ""
        );
      }
    );
  }, [formData, visitedSteps]);

  const signalCount = 28;

  /* =======================================================
     HANDLE INPUT CHANGE
  ======================================================= */

  const handleChange = (
    field,
    value
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));

    /*
      Mark the current step as visited
      once the user interacts with a field.
    */
    setVisitedSteps((prev) => {
      const updated = [...prev];

      updated[currentStep] = true;

      return updated;
    });

    setError("");
  };

  /* =======================================================
     NEXT STEP
  ======================================================= */

  const goNext = () => {
    if (
      currentStep <
      steps.length - 1
    ) {
      setCurrentStep(
        (prev) => prev + 1
      );
    } else {
      setReviewing(true);
    }
  };

  /* =======================================================
     BACK
  ======================================================= */

  const goBack = () => {
    if (reviewing) {
      setReviewing(false);
      setCurrentStep(
        steps.length - 1
      );
      return;
    }

    if (currentStep > 0) {
      setCurrentStep(
        (prev) => prev - 1
      );
    }
  };

  /* =======================================================
     ANALYZE RETURN
  ======================================================= */

  const analyzeReturn = async () => {
    setError("");
    setLoading(true);
    setResult(null);
    setAnalysisStage(0);

    const payload = {
      ...formData,
    };

    numericFields.forEach(
      (field) => {
        payload[field] =
          Number(payload[field]);
      }
    );

    let stage = 0;

    const interval =
      setInterval(() => {
        stage += 1;

        if (
          stage <
          analysisStages.length
        ) {
          setAnalysisStage(stage);
        }
      }, 650);

    try {
      const response =
        await fetch(
          "http://127.0.0.1:8000/predict",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify(
              payload
            ),
          }
        );

      if (!response.ok) {
        throw new Error(
          `Server returned ${response.status}`
        );
      }

      const data =
        await response.json();

      clearInterval(interval);

      setAnalysisStage(
        analysisStages.length
      );

      setTimeout(() => {
        setResult(data);
        setLoading(false);
      }, 500);
    } catch (err) {
      clearInterval(interval);

      setLoading(false);
      setAnalysisStage(-1);

      setError(
        "Unable to connect to the ReturnGuard risk engine. Make sure the FastAPI backend is running on port 8000."
      );
    }
  };

  /* =======================================================
     RESET
  ======================================================= */

  const resetAssessment = () => {
    setFormData(initialForm);

    setCurrentStep(0);

    setReviewing(false);

    setResult(null);

    setLoading(false);

    setError("");

    setAnalysisStage(-1);

    setVisitedSteps([
      false,
      false,
      false,
      false,
      false,
    ]);

    localStorage.removeItem(
      "returnguard-draft"
    );

    localStorage.removeItem(
      "returnguard-visited-steps"
    );
  };

  /* =======================================================
     RESULT VALUES
  ======================================================= */

  const riskScore =
    result?.risk_score ?? 0;

  const riskLevel =
    result?.risk_level ||
    "UNKNOWN";

  const decision =
    result?.decision || "—";

  const prediction =
    result?.prediction || "—";

  const abuseType =
    result?.abuse_type || "—";

  const abuseConfidence =
    result?.abuse_confidence !==
    undefined
      ? Math.round(
          Number(
            result.abuse_confidence
          ) * 100
        )
      : 0;

  const probability =
    result?.risk_probability !==
    undefined
      ? Math.round(
          Number(
            result.risk_probability
          ) * 100
        )
      : 0;

  /* =======================================================
     JSX
  ======================================================= */

  return (
    <div className="app-shell">

      {/* ===================================================
          HEADER
      =================================================== */}

      <header className="top-header">
        <div className="brand-area">

          <div className="brand-mark">
            RG
          </div>

          <div>
            <div className="brand-name">
              ReturnGuard AI
            </div>

            <div className="brand-subtitle">
              E-commerce Return Risk Intelligence
            </div>
          </div>

        </div>

        <div className="header-right">

          <button
            className="theme-toggle"
            onClick={() =>
              setDarkMode(
                (prev) => !prev
              )
            }
            aria-label="Toggle theme"
            title="Toggle theme"
          >
            {darkMode
              ? "☀"
              : "☾"}
          </button>

        </div>
      </header>

      {/* ===================================================
          MAIN
      =================================================== */}

      <main className="main-container">

        {/* =================================================
            FORM / INVESTIGATION
        ================================================= */}

        {!result &&
          !loading && (
            <>
              {/* ===========================================
                  INTRO
              =========================================== */}

              <section className="intro-section">

                <div>

                  <p className="eyebrow">
                    RETURN INVESTIGATION
                  </p>

                  <h1>
                    Assess return risk before approving a refund.
                  </h1>

                  <p className="intro-copy">
                    Evaluate customer,
                    transaction, return
                    behavior, verification
                    and historical risk
                    signals through a
                    single investigation
                    workflow.
                  </p>

                </div>

                <div className="investigation-card">

                  <div className="investigation-label">
                    INVESTIGATION ID
                  </div>

                  <div className="investigation-id">
                    {investigationId}
                  </div>

                  <div className="draft-status">
                    <span>●</span>

                    {signalCount}
                    {" "}
                    signals · Draft
                    saved automatically
                  </div>

                </div>

              </section>

              {/* ===========================================
                  STEPPER
              =========================================== */}

              <nav className="stepper">

                {steps.map(
                  (step, index) => {

                    const isActive =
                      index ===
                      currentStep;

                    const isComplete =
                      completedSteps[
                        index
                      ];

                    return (
                      <button
                        key={step.number}
                        className={`step-item ${
                          isActive
                            ? "active"
                            : ""
                        } ${
                          isComplete
                            ? "complete"
                            : ""
                        }`}
                        onClick={() => {
                          setCurrentStep(
                            index
                          );

                          setReviewing(
                            false
                          );
                        }}
                      >

                        <span className="step-number">
                          {isComplete
                            ? "✓"
                            : "○"}
                        </span>

                        <span className="step-text">

                          <small>
                            STEP{" "}
                            {step.number}
                          </small>

                          <strong>
                            {step.short}
                          </strong>

                        </span>

                      </button>
                    );
                  }
                )}

              </nav>

              {/* ===========================================
                  STEP FORM
              =========================================== */}

              {!reviewing && (
                <section className="investigation-panel">

                  <div className="panel-header">

                    <div>

                      <div className="panel-index">
                        STEP{" "}
                        {
                          steps[
                            currentStep
                          ].number
                        }
                      </div>

                      <h2>
                        {
                          steps[
                            currentStep
                          ].title
                        }
                      </h2>

                      <p>
                        {
                          steps[
                            currentStep
                          ].description
                        }
                      </p>

                    </div>

                    <div className="panel-progress">
                      <span>
                        {currentStep + 1}
                      </span>

                      <span>/</span>

                      <span>
                        {steps.length}
                      </span>
                    </div>

                  </div>

                  <div className="field-grid">

                    {steps[
                      currentStep
                    ].fields.map(
                      (field) => (
                        <Field
                          key={field}
                          field={field}
                          value={
                            formData[
                              field
                            ]
                          }
                          onChange={
                            handleChange
                          }
                        />
                      )
                    )}

                  </div>

                  {error && (
                    <div className="error-box">

                      <strong>
                        Risk engine error
                      </strong>

                      <span>
                        {error}
                      </span>

                    </div>
                  )}

                  <div className="navigation-row">

                    {currentStep > 0 ? (
                      <button
                        className="secondary-button"
                        onClick={
                          goBack
                        }
                      >
                        ← Previous
                      </button>
                    ) : (
                      <button
                        className="secondary-button"
                        onClick={
                          resetAssessment
                        }
                      >
                        Reset
                      </button>
                    )}

                    <button
                      className="primary-button"
                      onClick={goNext}
                    >
                      {currentStep ===
                      steps.length - 1
                        ? "Review Investigation →"
                        : "Continue →"}
                    </button>

                  </div>

                </section>
              )}

              {/* ===========================================
                  REVIEW SCREEN
              =========================================== */}

              {reviewing && (
                <section className="review-panel">

                  <div className="panel-header">

                    <div>

                      <div className="panel-index">
                        FINAL REVIEW
                      </div>

                      <h2>
                        Review Investigation
                      </h2>

                      <p>
                        Confirm all 28
                        signals before
                        sending the
                        investigation
                        to the risk
                        engine.
                      </p>

                    </div>

                    <div className="review-ready">

                      <span>
                        ✓
                      </span>

                      {signalCount}
                      {" "}
                      signals ready

                    </div>

                  </div>

                  <div className="review-sections">

                    {steps.map(
                      (
                        step,
                        index
                      ) => (

                        <div
                          className="review-section"
                          key={
                            step.number
                          }
                        >

                          <div className="review-section-header">

                            <div>

                              <span>
                                {
                                  step.number
                                }
                              </span>

                              <h3>
                                {
                                  step.title
                                }
                              </h3>

                            </div>

                            <button
                              onClick={() => {
                                setCurrentStep(
                                  index
                                );

                                setReviewing(
                                  false
                                );
                              }}
                            >
                              Edit
                            </button>

                          </div>

                          <div className="review-grid">

                            {step.fields.map(
                              (field) => {

                                const meta =
                                  fieldMeta[
                                    field
                                  ];

                                let displayValue =
                                  formData[
                                    field
                                  ];

                                if (
                                  meta.type ===
                                  "binary"
                                ) {
                                  displayValue =
                                    String(
                                      formData[
                                        field
                                      ]
                                    ) ===
                                    "1"
                                      ? "Yes"
                                      : "No";
                                }

                                return (
                                  <div
                                    className="review-field"
                                    key={
                                      field
                                    }
                                  >

                                    <span>
                                      {
                                        meta.label
                                      }
                                    </span>

                                    <strong>
                                      {
                                        displayValue ||
                                        "Not provided"
                                      }
                                    </strong>

                                  </div>
                                );
                              }
                            )}

                          </div>

                        </div>
                      )
                    )}

                  </div>

                  {error && (
                    <div className="error-box">

                      <strong>
                        Risk engine error
                      </strong>

                      <span>
                        {error}
                      </span>

                    </div>
                  )}

                  <div className="navigation-row">

                    <button
                      className="secondary-button"
                      onClick={
                        goBack
                      }
                    >
                      ← Back to Signals
                    </button>

                    <button
                      className="analyze-button"
                      onClick={
                        analyzeReturn
                      }
                    >

                      <span className="analyze-icon">
                        ◉
                      </span>

                      Analyze Return Risk

                    </button>

                  </div>

                </section>
              )}
            </>
          )}

        {/* =================================================
            ANALYSIS SCREEN
        ================================================= */}

        {loading && (
          <section className="analysis-console">

            <div className="analysis-orb">
              <div className="orb-core"></div>
            </div>

            <p className="eyebrow">
              RETURNGUARD ENGINE
            </p>

            <h1>
              Analyzing return investigation
            </h1>

            <p className="analysis-description">
              Evaluating 28 risk
              signals to determine
              the safest return
              action.
            </p>

            <div className="analysis-stages">

              {analysisStages.map(
                (
                  stage,
                  index
                ) => {

                  const completed =
                    index <
                    analysisStage;

                  const active =
                    index ===
                    analysisStage;

                  return (
                    <div
                      className={`analysis-stage ${
                        completed
                          ? "completed"
                          : ""
                      } ${
                        active
                          ? "active"
                          : ""
                      }`}
                      key={stage}
                    >

                      <span className="stage-icon">

                        {completed
                          ? "✓"
                          : active
                          ? "●"
                          : "○"}

                      </span>

                      <span>
                        {stage}
                      </span>

                      {active && (
                        <span className="stage-running">
                          RUNNING
                        </span>
                      )}

                    </div>
                  );
                }
              )}

            </div>

          </section>
        )}

        {/* =================================================
            RESULT DASHBOARD
        ================================================= */}

        {result &&
          !loading && (
            <section className="result-dashboard">

              <div className="result-top">

                <div>

                  <p className="eyebrow">
                    RETURN RISK ASSESSMENT
                  </p>

                  <h1>
                    Investigation complete.
                  </h1>

                  <p>
                    {investigationId}
                    {" "}
                    · 28 signals
                    evaluated
                  </p>

                </div>

                <div className="assessment-complete">

                  <span>
                    ✓
                  </span>

                  COMPLETE

                </div>

              </div>

              {/* =========================================
                  RISK OVERVIEW
              ========================================= */}

              <div className="risk-overview">

                <div className="score-card">

                  <div className="score-label">
                    RETURN RISK SCORE
                  </div>

                  <div className="score-number">

                    {riskScore}

                    <small>
                      /100
                    </small>

                  </div>

                  <div
                    className={`risk-badge ${riskLevel.toLowerCase()}`}
                  >
                    {riskLevel} RISK
                  </div>

                  <div className="score-track">

                    <div
                      className="score-fill"
                      style={{
                        width: `${Math.min(
                          100,
                          Math.max(
                            0,
                            Number(
                              riskScore
                            )
                          )
                        )}%`,
                      }}
                    ></div>

                  </div>

                  <div className="score-scale">

                    <span>
                      LOW
                    </span>

                    <span>
                      MEDIUM
                    </span>

                    <span>
                      HIGH
                    </span>

                  </div>

                </div>

                <div className="decision-card">

                  <div className="card-label">
                    RECOMMENDED ACTION
                  </div>

                  <div className="decision-main">
                    {decision}
                  </div>

                  <p>
                    ReturnGuard
                    recommends this
                    action based on
                    the combined
                    return-risk
                    assessment.
                  </p>

                  <div className="decision-rule">

                    <span>
                      ●
                    </span>

                    Automated risk policy

                  </div>

                </div>

              </div>

              {/* =========================================
                  RESULT METRICS
              ========================================= */}

              <div className="result-metrics">

                <div className="metric-card">

                  <span>
                    Prediction
                  </span>

                  <strong>
                    {prediction}
                  </strong>

                </div>

                <div className="metric-card">

                  <span>
                    Risk Probability
                  </span>

                  <strong>
                    {probability}%
                  </strong>

                </div>

                <div className="metric-card">

                  <span>
                    Abuse Pattern
                  </span>

                  <strong>
                    {abuseType}
                  </strong>

                </div>

                <div className="metric-card">

                  <span>
                    Pattern Confidence
                  </span>

                  <strong>
                    {abuseConfidence}%
                  </strong>

                </div>

              </div>

              {/* =========================================
                  MODEL EVIDENCE
              ========================================= */}

              <div className="evidence-panel">

                <div className="evidence-header">

                  <div>

                    <p className="eyebrow">
                      MODEL INTERPRETATION
                    </p>

                    <h2>
                      Risk Evidence
                    </h2>

                  </div>

                  <span className="evidence-count">
                    {signalCount}
                    {" "}
                    signals considered
                  </span>

                </div>

                <div className="evidence-grid">

                  <div className="evidence-item">

                    <span>
                      01
                    </span>

                    <div>

                      <strong>
                        Return behavior
                      </strong>

                      <p>
                        Historical
                        return activity
                        contributes to
                        the assessment.
                      </p>

                    </div>

                  </div>

                  <div className="evidence-item">

                    <span>
                      02
                    </span>

                    <div>

                      <strong>
                        Verification signals
                      </strong>

                      <p>
                        Evidence,
                        tracking and
                        packaging
                        signals are
                        evaluated
                        together.
                      </p>

                    </div>

                  </div>

                  <div className="evidence-item">

                    <span>
                      03
                    </span>

                    <div>

                      <strong>
                        Account risk
                      </strong>

                      <p>
                        Disputes,
                        account
                        patterns and
                        refund
                        anomalies
                        influence the
                        decision.
                      </p>

                    </div>

                  </div>

                  <div className="evidence-item">

                    <span>
                      04
                    </span>

                    <div>

                      <strong>
                        Transaction context
                      </strong>

                      <p>
                        Refund amount,
                        product and
                        payment
                        context are
                        included in
                        the risk model.
                      </p>

                    </div>

                  </div>

                </div>

              </div>

              {/* =========================================
                  RESULT FOOTER
              ========================================= */}

              <div className="result-footer">

                <button
                  className="secondary-button"
                  onClick={
                    resetAssessment
                  }
                >
                  + Start New Assessment
                </button>

                <div className="result-note">
                  ReturnGuard
                  provides a risk
                  recommendation,
                  not an irreversible
                  decision.
                </div>

              </div>

            </section>
          )}

      </main>

      {/* =================================================
          FOOTER
      ================================================= */}

      <footer className="footer">

        <div>

          <strong>
            ReturnGuard AI
          </strong>

          <span>
            Risk intelligence
            for e-commerce
            returns
          </span>

        </div>

        <span>
          Defense-only system ·
          AI Risk Manager
        </span>

      </footer>

    </div>
  );
}

export default App;