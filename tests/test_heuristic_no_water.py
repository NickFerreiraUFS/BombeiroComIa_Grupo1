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

    # distância até base = 2
    # distância base até fogo = 4
    # heurística retorna base_dist + fire_dist
    assert p.h(node) == 4
