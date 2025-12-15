def normalize_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def apply_rules(user: dict):
    """
    Robust admin rule engine.
    Accepts multiple key variants and always returns deterministic output.
    """

    actions = []
    reasons = []

    # Normalize inputs (accept all variants)
    reports = normalize_int(
        user.get("reports")
        or user.get("report_count")
        or user.get("reports_count")
    )

    trust = normalize_int(
        user.get("trust")
        or user.get("trust_score"),
        default=100
    )

    # RULE 1: Critical review
    if reports >= 3:
        actions.append("CRITICAL_REVIEW")
        reasons.append(f"User has {reports} reports (>=3)")

    # RULE 2: Escalation
    if trust < 40:
        actions.append("ESCALATE")
        reasons.append(f"Trust score is {trust} (<40)")

    return {
        "actions": actions,
        "reasons": reasons,
        "signals": {
            "reports": reports,
            "trust": trust
        }
    }
