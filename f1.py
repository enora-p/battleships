# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
def verify(grid,i,j):
    '''verifies if the ship is sunk or not'''
    idi = grid[i][j][1] #identifiant, unique to each ship to differenciate them (but the same for the cells of one ship)
    for k in range(len(grid[0])):
        for l in grid[k]:
            if type(l) == type(list()) and idi in l: #if a cell contains the ship that has been shot
                l[2] -= 1
    if grid[i][j][2] == 0:
        print("ship sunk")
    return grid

#how to differenciate cells from different ships ?
# [0] : state , 0 is unshot, 1 shot or boolean
# [1] : identifier , a string (or number if not from 0 to 5)            
# [0] : #celles of the ship (from 2 to 5)     
         
grid = [[0, [0,"a",2], [0,"a",2], 0, 0], [2, 2, 2, 2, 2], [0, 2, 0, 0, 0], [0, 0, 2, 0, 0], [0, 2, 0, 0, 0]]
i = 0 #int(input())
j = 1 #int(input())
if type(grid[i][j]) == type(list()): #there is a ship
    if grid[i][j][0]== 0:
        print("ship here")
        grid[i][j][0]+= 1
        verify(grid,i,j)#verify the boat is sunk or not
    else: #grid[i][j][0]== 1
        print("ship already shot")
else: #no ship
     grid[i][j] += 1 #shoot empty cell   


