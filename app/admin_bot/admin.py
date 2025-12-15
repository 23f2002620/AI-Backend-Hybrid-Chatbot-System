from app.admin_bot.rules import apply_rules
from app.admin_bot.retrieval import retrieve_policy_or_cases

def admin_bot(query: str, user: dict):
    rule_result = apply_rules(user)
    knowledge = retrieve_policy_or_cases(query)

    return {
        "actions": rule_result["actions"],
        "reasons": rule_result["reasons"],
        "signals": rule_result["signals"],
        "knowledge": knowledge
    }
