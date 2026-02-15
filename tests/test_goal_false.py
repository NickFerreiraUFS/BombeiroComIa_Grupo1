from problems.fire_problem import fireProblem

def test_goal_test_false():

    state = (
        (0,0),
        ((1,1)),   # ainda existe fogo
        2,
        (0,0)
    )

    p = fireProblem(
        initial=state,
        goal=None,
        grid=[[0]]
    )

    assert p.goal_test(state) == False
