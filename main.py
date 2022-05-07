import game

shapes = {"maman": [(False,True,False),(True,True,True)], "papa": [(True,False),(True,True),(True,False)]}

bat = game.battle(10, shapes, "moi", "toi", False, False)

bat.start()