from problems.fire_problem import fireProblem
from search import Node

def test_heuristic_with_water():

    state = (
        (0,0),
        ((2,2),),
        3,
        (0,0)
    )

    p = fireProblem(initial=state, goal=None, grid=[[0]*3 for _ in range(3)])

    node = Node(state)

    # distância Manhattan até (2,2)
    # |0-2| + |0-2| = 4
    assert p.h(node) == 4
