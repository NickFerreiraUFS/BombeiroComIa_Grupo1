from agents import Environment

class  FireEnvironment(Environment):
    def __init__(self, grid, initial_state):
        super().__init__()
        self.grid = grid
        self.state = initial_state
        self.base = (0, 0) 
        self.max_water = 3
        (_,_),fires,_,_ = self.state
        self.fires = list(fires)


    def percept(self, agent):
        return self.state

    def execute_action(self, agent, action):

        (x,y), _, water, base = self.state
        print(self.fires)
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
                print ("FOGO DETECTADO")
                self.fires.remove((x,y))
                self.state = ((x,y), tuple(self.fires), water-1, base)
                print("FOGO APAGADO")

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
