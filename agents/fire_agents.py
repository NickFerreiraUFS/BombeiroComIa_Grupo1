from agents import Agent
from search import astar_search
from problems.fire_problem import fireProblem

class FireAgent(Agent):

    def __init__(self, grid):

        self.grid = grid
        self.plan = []
        self.failed_state = None
        self.search_failed = False

        def program(percept):

            if not self.plan:
                # Avoid re-running the same failing search forever.
                if self.failed_state == percept:
                    self.search_failed = True
                    return "NoOp"

                problem = fireProblem(
                    initial = percept,
                    goal = None,
                    grid = self.grid
                )

                solution = astar_search(problem)

                if solution:
                    self.plan = solution.solution()
                    self.failed_state = None
                    self.search_failed = False
                else:
                    self.failed_state = percept
                    self.search_failed = True
                    return "NoOp"

            if self.plan:
                self.search_failed = False
                return self.plan.pop(0)

            return "NoOp"

        super().__init__(program)
