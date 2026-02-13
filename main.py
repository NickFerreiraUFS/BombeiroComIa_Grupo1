from problems.fire_problem import fireProblem
from search import astar_search

grid = [
    [".",".","."],
    [".","F","."],
    [".",".","."]
]

problem = fireProblem(
    initial=(0,0),
    goal=(2,2),
    grid=grid
)

solution = astar_search(problem)

print(solution.solution())
