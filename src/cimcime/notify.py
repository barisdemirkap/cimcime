from dataclasses import dataclass

from .approval_gate import ActionType

_ACTION_DESCRIPTIONS = {
    ActionType.PRODUCTION_DEPLOY: "a production-level delivery or deployment",
    ActionType.THIRD_PARTY_COMMUNICATION: "outbound communication to a real third party",
    ActionType.SPEND_OR_ACCOUNT_CHANGE: (
        "an action that spends real money or changes an external account/billing setting"
    ),
}


@dataclass(frozen=True)
class ApprovalGateHit:
    action: ActionType


@dataclass(frozen=True)
class Milestone:
    detail: str


NotificationEvent = ApprovalGateHit | Milestone


def format_notification(event: NotificationEvent) -> str:
    if isinstance(event, ApprovalGateHit):
        description = _ACTION_DESCRIPTIONS[event.action]
        return f"Approval needed: Cimcime is about to do {description} and is waiting for your go-ahead."
    if isinstance(event, Milestone):
        return f"Milestone: {event.detail}"
    raise TypeError(f"Unknown notification event: {event!r}")
