from search import Problem

class fireProblem(Problem):

    def __init__(self, initial, goal, grid, max_water=3):
        super().__init__(initial, goal)
        self.grid = grid
        self.max_water = max_water

    def path_cost(self, c, state1, action, state2):

        if action == "EXTINGUISH":
            return c + 2

        elif action == "REFILL":
            return c + 15   # 🔥 MUITO CARO AGORA

        else:
            return c + 1




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


    def h(self, node):
        pos, fires, water, base = node.state
        if not fires:
            return 0

        # 1. Distância para o fogo mais próximo (Admissível)
        dist_to_near_fire = min(abs(pos[0]-f[0]) + abs(pos[1]-f[1]) for f in fires)
        
        # 2. Se a água não for suficiente para todos os fogos, 
        # você OBRIGATORIAMENTE terá que ir à base pelo menos uma vez.
        base_penalty = 0
        if len(fires) > water:
            # Distância de onde estou até a base + custo do refill (15)
            dist_to_base = abs(pos[0]-base[0]) + abs(pos[1]-base[1])
            base_penalty = dist_to_base + 15
            
        return max(dist_to_near_fire, base_penalty)