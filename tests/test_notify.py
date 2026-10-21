from cimcime.approval_gate import ActionType
from cimcime.notify import ApprovalGateHit, Milestone, format_notification


def test_production_deploy_gate_hit_names_the_action_and_asks_for_go_ahead():
    message = format_notification(ApprovalGateHit(ActionType.PRODUCTION_DEPLOY))

    assert "production-level delivery or deployment" in message
    assert "waiting for your go-ahead" in message


def test_third_party_communication_gate_hit_names_the_action():
    message = format_notification(ApprovalGateHit(ActionType.THIRD_PARTY_COMMUNICATION))

    assert "outbound communication to a real third party" in message


def test_spend_or_account_change_gate_hit_names_the_action():
    message = format_notification(ApprovalGateHit(ActionType.SPEND_OR_ACCOUNT_CHANGE))

    assert "spends real money or changes an external account" in message


def test_milestone_carries_its_detail_text_through():
    message = format_notification(Milestone("Learning Phase complete, switched to Runtime Phase."))

    assert message == "Milestone: Learning Phase complete, switched to Runtime Phase."
