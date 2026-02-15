from agent.fire_agents import FireAgent

def test_agent_generates_plan():

    grid = [[0]*3 for _ in range(3)]

    state = (
        (0,0),
        ((1,1),),
        3,
        (0,0)
    )

    agent = FireAgent(grid)

    action = agent.program(state)

    assert action in ["UP", "DOWN", "LEFT", "RIGHT"]
