#import game

# bateau1 = game.ship("croiseur", [(False,True,False),(True,True,True)])
# bateau2 = game.ship("croiseur", [(True,False),(True,True),(True,False)])

# print(bateau1)

# game.ship.anticlockwise_rotate(bateau1)

# print(bateau1)

# a = list((x**2 for x in range(5)))

# [1, 2, 3]
# print(a)

shape = [(False,True,False),(True,True,True)]
ship_positions = {(i, j) for i, row in enumerate(shape) for j, cell in enumerate(row) if cell}
print(ship_positions)
ship_positions += (9,9)

print(ship_positions)
