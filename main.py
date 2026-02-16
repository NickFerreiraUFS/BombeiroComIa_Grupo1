from env.fire_env import FireEnvironment
from agent.fire_agents import FireAgent


grid = [
    [".",".",".","."],
    [".",".",".","."],
    [".",".",".","."],
    [".",".",".","."]
]

initial = (
    (2,2),
    ((1,1),(2,2),(2,3),(1,3),(3,3)),
     3,
    (0,0)
)

env = FireEnvironment(grid,initial)
agent = FireAgent(grid)

env.add_thing(agent)

while len(env.fires):
    env.step()
    env.render()

env.step()
env.render()