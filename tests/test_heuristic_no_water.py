from problems.fire_problem import fireProblem
from search import Node

def test_heuristic_without_water():

    state = (
        (1,1),
        ((2,2),),
        0,
        (0,0)
    )

    p = fireProblem(initial=state, goal=None, grid=[[0]*3 for _ in range(3)])

    node = Node(state)

    # dist_to_near_fire = 2
    # dist_to_base = 2
    # base_penalty = dist_to_base + 15 = 17
    # h = max(2, 17) = 17
    assert p.h(node) == 17
