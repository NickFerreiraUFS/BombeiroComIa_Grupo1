from agents import Agent
from problems.fire_problem import fireProblem
from search import InstrumentedProblem

class CompareAgent(Agent):
    def __init__(self, grid, search_alg):
        self.grid = grid
        self.search_alg = search_alg
        self.plan = []
        self.expanded = 0
        self.plan_cost = 0
        self.search_failed = False
        self.search_attempted = False
        self.last_state = None

        def program(percept):
            # Se a busca falhou e o estado mudou, libera nova tentativa.
            if self.search_failed and percept != self.last_state:
                self.search_failed = False
                self.search_attempted = False

            # Só planeja se não tiver plano e ainda não tentou para este estado.
            if not self.plan and not self.search_attempted and not self.search_failed:
                # Criamos o problema original
                problem = fireProblem(
                    initial=percept,
                    goal=None,
                    grid=self.grid
                )

                # Envolvemos com o InstrumentedProblem para contar os nós
                ip = InstrumentedProblem(problem)
                self.search_attempted = True

                # Executa o algoritmo de busca
                solution = self.search_alg(ip)
                self.expanded += ip.succs

                if solution:
                    self.plan = solution.solution()
                    self.plan_cost = solution.path_cost
                else:
                    self.search_failed = True

            # 🏃 Executa o próximo passo do plano
            if self.plan:
                action = self.plan.pop(0)

                # Permite replanejar se o plano acabar e ainda houver incêndios.
                if not self.plan:
                    self.search_attempted = False

                self.last_state = percept
                return action

            self.last_state = percept
            return "NoOp"

        super().__init__(program)
