from problems.fire_problem import fireProblem

def test_result_move_up():

    state = (
        (2,2),
        (),
        2,
        (0,0)
    )

    p = fireProblem(
        initial=state,
        goal=None,
        grid=[[0]*3 for _ in range(3)]
    )

    new_state = p.result(state, "UP")

    pos, _, _, _ = new_state

    assert pos == (1,2)
