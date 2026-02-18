from search import Problem

class fireProblem(Problem):

    def __init__(self, initial, goal, grid, max_water=3):
        super().__init__(initial, goal)
        self.grid = grid
        self.max_water = max_water


    def actions(self, state):

        (x,y), fires, water, base = state
        possible = []

        moves = {
            "UP": (x-1,y),
            "DOWN": (x+1,y),
            "LEFT": (x,y-1),
            "RIGHT": (x,y+1)
        }

        for action,(nx,ny) in moves.items():

            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                
                if water == 0 and (nx,ny) in fires:
                    continue

                possible.append(action)

        if (x,y) in fires and water > 0:
            possible.append("EXTINGUISH")

        if water == 0 and (x,y) == base:
            possible.append("REFILL")

        return possible



    def result(self, state, action):

        (x,y), fires, water, base = state
        fires = list(fires)

        if action == "UP":
            return ((x-1,y), tuple(fires), water, base)

        elif action == "DOWN":
            return ((x+1,y), tuple(fires), water, base)

        elif action == "LEFT":
            return ((x,y-1), tuple(fires), water, base)

        elif action == "RIGHT":
            return ((x,y+1), tuple(fires), water, base)

        elif action == "EXTINGUISH":
            fires.remove((x,y))
            return ((x,y), tuple(fires), water-1, base)

        elif action == "REFILL":
            return ((x,y), tuple(fires), self.max_water, base)


    def goal_test(self, state):
        pos, fires, water, base = state
        return len(fires) == 0


    def path_cost(self, c, s1, a, s2):
        return c + 1


    def h(self, node):

        (x,y), fires, water, base = node.state

        if not fires:
            return 0

        fire_dist = min(
            abs(x-fx) + abs(y-fy)
            for (fx,fy) in fires
        )

        if water > 0:
            return fire_dist

        base_dist = abs(x-base[0]) + abs(y-base[1])

        return base_dist + fire_dist

