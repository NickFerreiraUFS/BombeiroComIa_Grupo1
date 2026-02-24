from env.fire_env import FireEnvironment
from agents.fire_agents import FireAgent
import time


grid = [["." for _ in range(10)] for _ in range(10)]

initial = (
    (0, 0),
    ((5, 5), (5, 9), (9, 5), (9, 9), (7, 7), (2, 9), (9, 2)),
    3,
    (0, 0)
)

env = FireEnvironment(grid, initial)
agent = FireAgent(grid)

env.add_thing(agent)

STEP_DELAY = 0.1

while len(env.fires) and not agent.search_failed:
    env.step()
    env.render()
    time.sleep(STEP_DELAY)

env.step()
env.render()

if agent.search_failed and len(env.fires) > 0:
    print("Busca falhou para o estado atual; encerrando para evitar loop infinito.")
