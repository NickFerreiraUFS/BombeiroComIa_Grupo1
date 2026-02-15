from problems.fire_problem import fireProblem

def test_goal_test_true():

    state = ((0,0), (), 2, (0,0))

    p = fireProblem(
        initial=state,
        goal=None,
        grid=[[0]]
    )

    assert p.goal_test(state) == True
