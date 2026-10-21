from cimcime.approval_gate import ActionType, requires_approval


def test_production_deploy_requires_approval():
    assert requires_approval(ActionType.PRODUCTION_DEPLOY) is True


def test_third_party_communication_requires_approval():
    assert requires_approval(ActionType.THIRD_PARTY_COMMUNICATION) is True


def test_spend_or_account_change_requires_approval():
    assert requires_approval(ActionType.SPEND_OR_ACCOUNT_CHANGE) is True


def test_routine_work_does_not_require_approval():
    assert requires_approval(ActionType.ROUTINE_WORK) is False
