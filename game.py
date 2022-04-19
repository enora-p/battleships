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
    
    def place(self, xpos: int, ypos: int):
        self.anchor = ypos, xpos
        self.positions = {}
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    cellpos = (ypos + i, xpos + j)
                    self.positions[cellpos] = True
        self.placed = True

    def hit(self, xtar: int, ytar: int):
        assert self.positions[(ytar, xtar)], "Position already hit."

        self.positions[(ytar, xtar)] = False
        if not (True in self.positions.values()):
            self.sunk = True
            return 's'
        
        return 'h'


class player:
    def __init__(self, name: str, gridsize: int, ships = list[ship], isAI: bool = False):
        self.name = name
        self.ships = ships
        self.isAI = isAI
        self.alive = True
        self.opponent = None
        self.tracking = [['w'] * gridsize] * gridsize

    def set_opponent(self, opponent: 'player'):
        self.opponent = opponent

    def play(self):
        if self.isAI:
            pass
        else:
            target_invalid = True
            while target_invalid:
                xtar, ytar = int(input("Target horizontal position: ")), int(input("Target vertical position: "))
                
                if not (0 <= xtar < len(self.tracking[0])) or not (0 <= ytar < len(self.tracking)):
                    target_invalid = True
                    print("Target is out of bounds, please try again.")
                elif self.tracking[ytar][xtar] in "mhs":
                    target_invalid = True
                    print("Target has already been hit, please try again.")
                else:
                    target_invalid = False
            
            hit, ship_index = self.opponent.get_shot(xtar, ytar)
            self.tracking[ytar][xtar] = hit

            if hit == 's':
                for ypos, xpos in self.opponent.ships[ship_index].positions.keys():
                    self.tracking[ypos][xpos] = 's'

    def get_shot(self, xtar: int, ytar: int):
        hit = 'm'
        for idx, ship in enumerate(self.ships):
            if (ytar, xtar) in ship.positions.keys():
                hit = ship.hit(xtar, ytar)
        
        if hit == 'm':
            print("MISS!")
        elif hit == 'h':
            print("HIT!")
        else:
            print("SUNK!")

        return (hit, idx)

class battle:
    def __init__(self, gridsize, ships, player1isAI, player2isAI):
        pass