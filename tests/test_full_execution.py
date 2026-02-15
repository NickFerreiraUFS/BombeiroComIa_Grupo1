from env.fire_env import FireEnvironment
from agent.fire_agents import FireAgent

def test_full_execution():

    grid = [[0]*3 for _ in range(3)]

    initial = (
        (0,0),
        ((1,1),),
        3,
        (0,0)
    )

    env = FireEnvironment(grid, initial)
    agent = FireAgent(grid)

    env.add_thing(agent)

    # executa alguns passos
    for _ in range(10):
        env.step()

    assert len(env.fires) == 0
