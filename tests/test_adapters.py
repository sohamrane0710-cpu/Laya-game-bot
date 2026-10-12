
from adapters.doom.state_adapter import DoomStateAdapter
from adapters.doom.decision_adapter import DoomDecisionAdapter
from safety.validator import ActionValidator


def test_state_adapter():
    class FakeState:
        number = 10
        game_variables = [75.0, 12.0]

    state = DoomStateAdapter().transform(FakeState())

    assert state["health"] == 75.0
    assert state["ammo"] == 12.0
    assert state["step"] == 10
    assert "attack" in state["available_actions"]


def test_decision_adapter():
    adapter = DoomDecisionAdapter()

    assert adapter.transform("attack") == "attack"


def test_validator_accepts_valid_action():
    adapter = DoomDecisionAdapter()
    validator = ActionValidator(adapter.allowed_actions)

    valid, reason = validator.validate("attack")

    assert valid is True
    assert reason is None


def test_validator_rejects_invalid_action():
    adapter = DoomDecisionAdapter()
    validator = ActionValidator(adapter.allowed_actions)

    valid, reason = validator.validate("delete_everything")

    assert valid is False
    assert reason is not None
