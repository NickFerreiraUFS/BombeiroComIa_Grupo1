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

        def program(percept):
            # Só planeja se ainda não tiver um plano na memória
            if not self.plan:
                # Criamos o problema original
                problem = fireProblem(
                    initial=percept,
                    goal=None,
                    grid=self.grid
                )
                
                # Envolvemos com o InstrumentedProblem para contar os nós
                ip = InstrumentedProblem(problem)

                # Executa o algoritmo de busca
                solution = self.search_alg(ip)

                if solution:
                    self.plan = solution.solution()
                    self.plan_cost = solution.path_cost
                    # .succs conta quantas vezes o algoritmo expandiu estados
                    self.expanded = ip.succs 

            # 🏃 Executa o próximo passo do plano
            if self.plan:
                return self.plan.pop(0)

            return "NoOp"

        super().__init__(program)