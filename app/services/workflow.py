VALID_STATUSES = {"new", "processing", "waiting_customer", "resolved", "closed"}

ALLOWED_TRANSITIONS = {
    "new": {"processing", "closed"},
    "processing": {"waiting_customer", "resolved", "closed"},
    "waiting_customer": {"processing", "resolved", "closed"},
    "resolved": {"closed", "processing"},
    "closed": set(),
}


def can_transition(current: str, target: str) -> bool:
    if target not in VALID_STATUSES:
        return False
    if current == target:
        return True
    return target in ALLOWED_TRANSITIONS.get(current, set())
