def get_risk_factors(data):
    factors = []

    # Strong model-supported signals
    if data["return_rate_pct"] > 30:
        factors.append("High historical return rate")

    if data["total_returns_lifetime"] > 10:
        factors.append("High number of previous returns")

    if data["customer_support_contacts"] >= 3:
        factors.append("Frequent customer support contacts")

    if data["previous_dispute_count"] > 0:
        factors.append("Previous disputes detected")

    if data["refund_to_different_account"] == 1:
        factors.append("Refund requested to a different account")

    if data["multiple_accounts_flag"] == 1:
        factors.append("Multiple accounts detected")

    if data["item_returned_opened"] == 1:
        factors.append("Returned item was opened")

    if data["refund_amount_requested_usd"] > 300:
        factors.append("High refund amount requested")

    if data["tracking_number_valid"] == 0:
        factors.append("Tracking number could not be validated")

    # Keep the dashboard concise
    return factors[:5]