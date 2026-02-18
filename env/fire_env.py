from agents import Environment

class  FireEnvironment(Environment):
    def __init__(self, grid, initial_state, max_water=None):
        super().__init__()
        self.grid = grid
        self.state = initial_state
        (_,_), fires, initial_water, base = self.state
        self.base = base
        self.max_water = initial_water if max_water is None else max_water
        self.fires = list(fires)


    def percept(self, agent):
        return self.state

    def execute_action(self, agent, action):

        (x,y), _, water, base = self.state
        if action == "UP":
            self.state = ((x-1,y), tuple(self.fires), water, base)

        elif action == "DOWN":
            self.state = ((x+1,y), tuple(self.fires), water, base)

        elif action == "LEFT":
            self.state = ((x,y-1), tuple(self.fires), water, base)

        elif action == "RIGHT":
            self.state = ((x,y+1), tuple(self.fires), water, base)

        elif action == "EXTINGUISH":
            if (x,y) in self.fires and water > 0:
                self.fires.remove((x,y))
                self.state = ((x,y), tuple(self.fires), water-1, base)

        elif action == "REFILL":
            if (x,y) == base:
                self.state = ((x,y), tuple(self.fires), self.max_water, base)


    def render(self):

        (bx,by), fires, water, base = self.state

        for i in range(len(self.grid)):
            row = ""
            for j in range(len(self.grid[0])):

                if (i,j) == (bx,by):
                    row += "B "
                elif (i,j) in fires:
                    row += "F "
                elif (i,j) == base:
                    row += "W "
                else:
                    row += ". "

            print(row)

        print("Água:",water)
        print("-------------------")
