from agents.compare_agent import CompareAgent


def test_compare_agent_does_not_repeat_failed_search_on_same_state():
    calls = {"count": 0}

    def failing_search(_problem):
        calls["count"] += 1
        return None

    grid = [[0]]
    state = ((0, 0), ((0, 0),), 0, (0, 0))
    agent = CompareAgent(grid, failing_search)

    assert agent.program(state) == "NoOp"
    assert agent.program(state) == "NoOp"
    assert calls["count"] == 1


def test_compare_agent_retries_search_if_state_changes_after_failure():
    calls = {"count": 0}

    def failing_search(_problem):
        calls["count"] += 1
        return None

    grid = [[0, 0]]
    state = ((0, 0), ((0, 1),), 0, (0, 0))
    new_state = ((0, 1), ((0, 1),), 0, (0, 0))
    agent = CompareAgent(grid, failing_search)

    assert agent.program(state) == "NoOp"
    assert agent.program(new_state) == "NoOp"
    assert calls["count"] == 2
