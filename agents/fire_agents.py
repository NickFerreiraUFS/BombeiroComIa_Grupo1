from agents import Agent
from problems.fire_problem import FireProblem
from search import astar_search

class FireAgent(Agent):

    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.plan = []

    def progam(self,percept):
        if not self.plan:

            problem = FireProblem(
                initial=percept,
                goal = None,
                grid=self.grid
            )

            solution = astar_search(problem)
            self.plan = solution.solution()

        return self.plan.pop(0)