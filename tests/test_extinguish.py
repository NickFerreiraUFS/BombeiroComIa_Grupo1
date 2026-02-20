from problems.fire_problem import fireProblem

def test_result_extinguish_removes_fire():

    state = (
        (1,1),
        ((1,1),),
        2,
        (0,0)
    )

    p = fireProblem(
        initial=state,
        goal=None,
        grid=[[0]*3 for _ in range(3)]
    )

    new_state = p.result(state, "EXTINGUISH")

    pos, fires, water, base = new_state

    assert (1,1) not in fires
    assert water == 1
