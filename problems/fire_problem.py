from search import Problem

class fireProblem(Problem):

    def __init__(self, initial, goal, grid):
        super().__init__(initial, goal)
        self.grid = grid

    def actions(self, state):
        x, y = state
        possible = []

        moves = {
            "UP": (x-1, y),
            "DOWN": (x+1, y),
            "LEFT": (x, y-1),
            "RIGHT": (x, y+1)
        }

        for action, (nx, ny) in moves.items():

            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):

                if self.grid[nx][ny] != "X":   # NÃO é parede
                    possible.append(action)

        return possible

    
    def result(self, state, action):
        x, y = state

        if action == "UP":
            return (x-1, y)
        elif action == "DOWN":
            return (x+1, y)
        elif action == "LEFT":
            return (x, y-1)
        elif action == "RIGHT":
            return (x, y+1)
    
    def goal_test(self, state):
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def h(self, node):
        x1, y1 = node.state
        x2, y2 = self.goal

        return abs(x1-x2) + abs(y1-y2)

