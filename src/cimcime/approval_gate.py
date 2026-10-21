from enum import Enum


class ActionType(str, Enum):
    PRODUCTION_DEPLOY = "production_deploy"
    THIRD_PARTY_COMMUNICATION = "third_party_communication"
    SPEND_OR_ACCOUNT_CHANGE = "spend_or_account_change"
    ROUTINE_WORK = "routine_work"


_GATED = frozenset(
    {
        ActionType.PRODUCTION_DEPLOY,
        ActionType.THIRD_PARTY_COMMUNICATION,
        ActionType.SPEND_OR_ACCOUNT_CHANGE,
    }
)


def requires_approval(action: ActionType) -> bool:
    return action in _GATED
