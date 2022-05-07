class ship:
    def __init__(self, name: str, shape: list[tuple[bool, ...]]):
        self.name = name
        self.shape = shape
        self.sunk = False
        self.placed = False

    def __str__(self):
        lines = [" __"*len(self.shape[0])] + ["|" + "".join(["██|" if cell else "__|" for cell in row]) for row in self.shape]
        return "\n".join(lines)

    def clockwise_rotate(self):
        assert not self.placed, "Ship is anchored, cannot be rotated anymore!"

        self.shape = list(zip(*self.shape[::-1]))

    def anticlockwise_rotate(self):
        assert not self.placed, "Ship is anchored, cannot be rotated anymore!"
        
        self.shape = list(zip(*self.shape))[::-1]
    
    def place(self, positions: set[tuple[int, int]]):
        self.positions = {cellpos: True for cellpos in positions}
        self.placed = True

    def damage(self, xtar: int, ytar: int):
        assert (ytar, xtar) in self.positions.keys(), "Position already hit."

        self.positions[(ytar, xtar)] = False
        if not (True in self.positions.values()):
            hit = 'S'
            self.sunk = True
        else:
            hit = 'H'
        
        return hit


class player:
    def __init__(self, name: str, gridsize: int, ships: list[ship], isAI: bool = False):
        self.name = name
        self.ships = ships
        self.isAI = isAI
        self.alive = True
        self.opponent = None
        self.map = [["WU"] * gridsize for _ in range(gridsize)]
    
    def strmap(self, *, full: bool = False):
        if full:
            lines = ["  " + ''.join([f" {j:02}" for j in range(len(self.map[0]))])] + \
                    [f"{i} |" + ''.join(["__|" if cell[:-1] == 'W' else "██|" for cell in row]) for i, row in enumerate(self.map)]
        else:
            lines = ["  " + ''.join([f" {j:02}" for j in range(len(self.map[0]))])] + \
                    [f"{i} |" + ''.join(["__|" if cell[-1] == 'U' else "OO|" if cell[-1] == 'M' else "░░|" if cell[-1] == "H" else "╬╬|" for cell in row]) for i, row in enumerate(self.map)]
        
        return "\n".join(lines)

    def set_opponent(self, opponent: 'player'):
        self.opponent = opponent
    
    def setup(self):
        if self.isAI:
            pass
        else:
            print(self.strmap(full=True))
            placed_positions = set()
            for idx, ship in enumerate(self.ships):
                placement_invalid = True
                while placement_invalid:
                    xpos, ypos = int(input("Anchor horizontal position: ")), int(input("Anchor vertical position: "))    
                    ship_positions = {(ypos + i, xpos + j) for i, row in enumerate(ship.shape) for j, cell in enumerate(row) if cell}
                    
                    if not (0 <= xpos < len(self.map[0]) and 0 <= ypos < len(self.map)):
                        print("Cannot place ship out of bounds, please try again.")
                    elif not placed_positions.isdisjoint(ship_positions):
                        print("Cannot have ships overlapping, please try again.")
                    else:
                        placement_invalid = False
                        for ypos, xpos in ship_positions:
                            if not (0 <= xpos < len(self.map[0]) and 0 <= ypos < len(self.map)):
                                placement_invalid = True
                        
                        if placement_invalid:
                            print("Cannot place ship out of bounds, please try again.")

                for ypos, xpos in ship_positions:
                    self.map[ypos][xpos] = str(idx) + 'U'
                    for line in self.map: print(line)
                
                ship.place(ship_positions)
                placed_positions.update(ship_positions)
                print(self.strmap(full=True))
                print(f"{self.name}'s ship, {ship.name} #{idx} has been successfully placed!")

    def play(self):
        if self.isAI:
            pass
        else:
            target_invalid = True
            while target_invalid:
                print(self.opponent.strmap())
                xtar, ytar = int(input("Target horizontal position: ")), int(input("Target vertical position: "))
                
                if not (0 <= xtar < len(self.opponent.map[0])) or not (0 <= ytar < len(self.opponent.map)):
                    target_invalid = True
                    print("Target is out of bounds, please try again.")
                elif self.opponent.map[ytar][xtar][-1] != 'U':
                    target_invalid = True
                    print("Target has already been hit, please try again.")
                else:
                    target_invalid = False
            
            self.opponent.get_shot(xtar, ytar)

    def get_shot(self, xtar: int, ytar: int):
        assert self.map[ytar][xtar][-1] == 'U', "Position already hit."

        if self.map[ytar][xtar][:-1] == 'W':
            self.map[ytar][xtar] = self.map[ytar][xtar][:-1] + 'M'
            print("MISS!")
        else:
            id = self.map[ytar][xtar][:-1]
            hit = self.ships[int(id)].damage(xtar, ytar)
            self.map[ytar][xtar] = id + hit

            if hit == 'S':
                for ypos, xpos in self.ships[int(id)].positions.keys():
                    self.map[ypos][xpos] = self.map[ypos][xpos][:-1] + hit
                print("SUNK!")

                self.alive = False
                i, n = 0, len(self.ships)
                while not self.alive and i < n:
                    if not self.ships[i].sunk:
                        self.alive = True
                    else: i += 1
            else:
                print("HIT!")

class battle:
    def __init__(self, gridsize: int, possible_ships: dict[str, list[tuple[bool, ...]]], P1_name: str, P2_name: str, P1isAI: bool = False, P2isAI: bool = False):
        self.gridzise = gridsize

        P1_ships = [ship(name, shape) for name, shape in possible_ships.items()]
        P2_ships = [ship(name, shape) for name, shape in possible_ships.items()]

        self.player1 = player(P1_name, gridsize, P1_ships, P1isAI)
        self.player2 = player(P2_name, gridsize, P2_ships, P2isAI)

        self.player1.set_opponent(self.player2)
        self.player2.set_opponent(self.player1)
    
    def start(self):
        # Ship placement procedure
        self.player1.setup()
        self.player2.setup()

        # Start of actual game
        winner = None
        while winner is None:
            self.player1.play()
            if not self.player2.alive:
                winner = self.player1
            else:
                self.player2.play()
                if not self.player1.alive:
                    winner = self.player2
        
        print(f"{winner.name} won the game! Congrats!")