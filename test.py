from main import *

field = Playfield(3)
pl1 = Player(field, 1, (0,0), symbol = '■')
pl2 = Player(field, 2, (2,2), symbol = '§')

field.display()
