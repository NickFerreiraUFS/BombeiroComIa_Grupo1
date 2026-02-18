import time
from env.fire_env import FireEnvironment
from agents.compare_agent import CompareAgent

from search import (
    astar_search,
    breadth_first_graph_search,
    depth_first_graph_search,
    uniform_cost_search,
    greedy_best_first_graph_search
)

grid = [["." for _ in range(20)] for _ in range(20)]

initial = (
    (0, 0), 
    ((5, 5), (5, 15), (15, 5), (15, 15), (10, 10), (2, 18), (18, 2)), 
    3, 
    (0, 0)
)

algorithms = {
    "BFS": lambda p: breadth_first_graph_search(p),
    "DFS": lambda p: depth_first_graph_search(p),
    "UCS": lambda p: uniform_cost_search(p),
    "Greedy": lambda p: greedy_best_first_graph_search(p, lambda n: p.h(n)),
    "A*": lambda p: astar_search(p)
}


results = []


for name, alg in algorithms.items():

    print(f"\nRodando {name}...")

    env = FireEnvironment(grid, initial)
    agent = CompareAgent(grid, alg)
    env.add_thing(agent)

    start = time.time()

    steps = 0

    # roda até acabar os fogos OU até limite de segurança
    max_steps = 1000

    while len(env.state[1]) > 0 and steps < max_steps:
        env.step()
        steps += 1
    cost = agent.plan_cost
    end = time.time()

    if steps >= max_steps:
        results.append((name, "TIMEOUT", "TIMEOUT"))
    else:
        results.append((name, steps, cost, round(end-start,4), agent.expanded))

cost = agent.plan_cost


print("\n===== RESULTADOS =====")
for r in results:
    print(f"{r[0]} -> Passos: {r[1]} | Custo: {r[2]} | Tempo: {r[3]}s | Nós: {r[4]}")

