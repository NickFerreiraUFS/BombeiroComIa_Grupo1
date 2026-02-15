from problems.fire_problem import fireProblem

def test_result_refill():

    state = (
        (0,0),
        ((1,1),),
        3,
        (0,0)
    )

    p = fireProblem(
        initial=state,
        goal=None,
        grid=[[0]]
    )

    new_state = p.result(state, "REFILL")

    pos, fires, water, base = new_state

    assert water == 3
