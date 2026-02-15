from problems.fire_problem import fireProblem

def test_path_cost():

    p = fireProblem(
        initial=None,
        goal=None,
        grid=[[0]]
    )

    cost = p.path_cost(5, None, None, None)

    assert cost == 6
