from problems.fire_problem import fireProblem

def test_path_cost_for_actions():

    p = fireProblem(
        initial=None,
        goal=None,
        grid=[[0]]
    )

    assert p.path_cost(0, None, "UP", None) == 1
    assert p.path_cost(0, None, "EXTINGUISH", None) == 2
    assert p.path_cost(0, None, "REFILL", None) == 15
