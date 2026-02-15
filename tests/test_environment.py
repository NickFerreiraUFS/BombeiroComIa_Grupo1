from env.fire_env import FireEnvironment

def test_environment_extinguish():

    grid = [[0]*3 for _ in range(3)]

    state = (
        (1,1),
        ((1,1),),
        3,
        (0,0)
    )

    env = FireEnvironment(grid, state)

    class DummyAgent:
        pass

    agent = DummyAgent()

    env.execute_action(agent, "EXTINGUISH")

    (_, fires, water, _) = env.state

    assert len(fires) == 0
    assert water == 2
