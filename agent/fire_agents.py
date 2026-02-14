from agents import Agent
from search import astar_search
from problems.fire_problem import fireProblem

class FireAgent(Agent):

    def __init__(self, grid):

        self.grid = grid
        self.plan = []
        self.last_state = None

        def program(percept):

            # 🔥 Se o mundo mudou → joga plano fora
            if percept != self.last_state:
                self.plan = []

            self.last_state = percept

            # 🧠 Replaneja se não tem plano
            if not self.plan:

                problem = fireProblem(
                    initial = percept,
                    goal = None,
                    grid = self.grid
                )

                solution = astar_search(problem)

                if solution:
                    self.plan = solution.solution()

            if self.plan:
                return self.plan.pop(0)

            return "NoOp"

        super().__init__(program)
