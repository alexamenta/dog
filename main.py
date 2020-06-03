max_players = 2

# the list of valid (but not necessarily legal) moves
valid_movestrings = {'W', 'E', 'N', 'S',
                     'WW', 'EE', 'NN', 'SS',
                     'NW', 'NE', 'SW', 'SE'}

class IllegalMove(Exception):
    pass

def check_legality(player, movestring):
    "Raises IllegalMove if the proposed move is illegal"

    if not movestring in valid_movestrings:
        raise IllegalMove

    new_position = calculate_move(player, movestring)

    # the new position must be on the playfield
    if not new_position in player.field.points:
        raise IllegalMove

    if player.field.is_occupied(new_position):
        raise IllegalMove


def move_vector(move_string):
    "Given a move string, calculate the move vector"
    vector_dict = {'W': (-1,0),
                   'E': (1,0),
                   'N': (0,1),
                   'S': (0,-1)}

    move_vector_x = 0
    move_vector_y = 0

    for char in move_string:
        move_vector_x += vector_dict[char][0]
        move_vector_y += vector_dict[char][1]

    return (move_vector_x, move_vector_y)


def calculate_move(player, move_string):
    "Given a player and a move string, calculate the new position"

    new_position_x = player.position[0] + move_vector(move_string)[0]
    new_position_y = player.position[1] + move_vector(move_string)[1]

    return (new_position_x, new_position_y)





class Playfield:
    """
    The field of play. Initialises as a square of specified sidelength
    (default 10)
    """
    def __init__(self, size=10):
        self.size = size
        self.points = {(x,y) for x in range(size) for y in range(size)}
        self.players = []

    def contains(self, point):
        "Checks whether the playfield contains a given point."
        return point in self.points

    def is_occupied(self, point):
        "Checks whether the given point is occupied by a player."
        return any(pl.position == point for pl in self.players)

    def remove(self, point):
        """
        Remove specified point from the playfield.
        Returns an error if the point is not in the playfield.
        """
        assert self.contains(point), (
            'Specified point not contained in playfield')
        self.points.remove(point)

    def display(self, present_symbol='·', absent_symbol=' '):
        """
        Displays the playfield.
        The characters used to denote whether a point or player is present
        can be specified as optional arguments.
        """

        size = self.size

        display_dict = {True: present_symbol, False: absent_symbol}
        display_string = ""

        # generate the string to be displayed
        # first generate the view of the playfield

        display_string += '╔' + '═'*size + '╗\n'

        for y in reversed(range(size)):
            display_string += '║'
            for x in range(size):
                
                # if a player is present, draw its symbol
                for pl in self.players:

                    if (x,y) == pl.position:
                        display_string += pl.symbol
                        break
                
                # otherwise, draw the present or absent symbol
                else:
                    display_string += display_dict[(x,y) in self.points]
                
            display_string += '║\n'

        display_string += '╚' + '═'*size + '╝'

        # generate list of players
        player_string = "\n  Players: \n"
        for pl in self.players:
            player_string += "{}: {} | ".format(pl.symbol, pl.id)

        display_string += player_string
                         
        # display the playfield string
        print(display_string)

        
class Player:
    """
    Represents one of the two players.
    """
    def __init__(self, field, id, position, symbol = '■'):
        assert len(field.players) < max_players, (
            'Field can contain maximum {} players'.format(max_players))
        self.field = field
        self.id = id
        self.symbol = symbol

        assert position in field.points, (
            'Player position must be on the playfield')
        self.position = position

        # add player to the list of players on the playfield
        self.field.players.append(self)

    def move(self, movestring):
        try:
            check_legality(self, movestring)
            old_position = self.position
            self.position = calculate_move(self, movestring)
            self.field.remove(old_position)
        except:
            print("Illegal move")

    def has_legal_moves(self):
        "Checks whether the player has any legal moves using Exceptions."
        for ms in valid_movestrings:
            try:
                check_legality(self, ms)
                return True
            except IllegalMove:
                pass

        return False
                
        

class Game:
    "A game of Dog."
    def __init__(self, size, p1_name, p2_name):
        
        self.field = Playfield(size)

        p1 = Player(self.field, p1_name, (0,0), '@')
        p2 = Player(self.field, p2_name, (size-1, size-1), 'Ð')
        
        self.players = [p1, p2]

        
    def play(self):
        "Play a game of Dog"

        import time, random

        print('Flipping a fair coin...')  
        time.sleep(1)
        current = random.randint(0,1)
        print('{} moves first.'.format(self.players[current].id))
        time.sleep(1)

        # gameplay loop, while the current player has legal moves
        while self.players[current].has_legal_moves() == True:
            print('\n'*5)
            print('-'*32)
            self.field.display()
            player = self.players[current]
            ms = input("{}, enter your move: ".format(player.id))
            
            try:
                check_legality(player, ms)
                player.move(ms)
                current = (current + 1) % 2
            except IllegalMove:
                print("That's not a legal move!")
                

        # at this point, the current player has no legal moves, and the
        # other player wins
                
        self.field.display()
                
        loser = self.players[current]
        winner = self.players[(current + 1) % 2]
                
        print("!"*10)
        time.sleep(1)
        print("{} has no legal moves!".format(loser.id))
        time.sleep(1)
        print("{} blacked out!".format(loser.id))
        time.sleep(1.5)
        print("{} wins!".format(winner.id))
        time.sleep(3)
        print("bye")

        
def play_dog():

    print("~~~~DOG~~~~ (v0.2)")

    pl1_name = input("Player 1, enter your name: ")
    pl2_name = input("Player 2, enter your name: ")
    size = int(input("Enter board size (positive integer please): "))
    # make sure this is greater than 1

    game = Game(size, pl1_name, pl2_name)
    game.play()

if __name__ == "__main__":
    play_dog()

            

        
