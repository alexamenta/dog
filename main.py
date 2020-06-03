import time, random, re

class IllegalMove(Exception):
    "Exception raised when a proposed move is illegal."
    pass

class InvalidMovestring(Exception):
    "Exception raised when a given movestring is invalid."

def is_legal(player, dest):
    "True if dest is a legal move for player; False otherwise"

    if not dest in player.field.points:
        return False

    if player.field.is_occupied(dest):
        return False

    if not 1 <= player.distance(dest) <= 2:
        return False

    return True

    
def process_movestring(ms):
    """
    Removes all spaces and capitalises an input string.
    Raises InvalidMovestring if the movestring is invalid.
    """
    stripped_ms = ms.upper().replace(" ", "")
    if not re.fullmatch("[NEWS]+", stripped_ms):
        raise InvalidMovestring
    return stripped_ms
    

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

def calculate_dest(player, move_string):
    "Given a player and a move string, calculate the destination"

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
    Represents a player.
    """
    def __init__(self, field, id, position, symbol = '■'):
        assert len(field.players) < 2, 'Field can contain maximum 2 players'
        self.field = field
        self.id = id
        self.symbol = symbol

        assert position in field.points, (
            'Player position must be on the playfield')
        self.position = position

        self.field.players.append(self)

    def distance(self, dest):
        """
        Gives the (Manhattan) distance from the player's position 
        to a destination.
        """
        delta_x = abs(self.position[0] - dest[0])
        delta_y = abs(self.position[1] - dest[1])
        return delta_x + delta_y

    def legal_destinations(self):
        "Lists the points in the playfield to which the player can move."
        return [pt for pt in self.field.points if is_legal(self, pt)]

    def move(self, dest):
        "Moves the player to a target destination, if the move is legal."
        if is_legal(self, dest):
            old_position = self.position
            self.position = dest
            self.field.remove(old_position)
        else:
            raise IllegalMove
                
        
class Game:
    "A game of Dog."
    def __init__(self, size, p1_name, p2_name):
        
        self.field = Playfield(size)

        p1 = Player(self.field, p1_name, (0,0), '@')
        p2 = Player(self.field, p2_name, (size-1, size-1), 'Ð')
        
        self.players = [p1, p2]

        print('Flipping a fair coin...')  
        time.sleep(1)
        
        self.current_player = random.choice(self.players)
        print(f'{self.current_player.id} moves first.')
        time.sleep(1)
    
    def current_player_index(self):
        "Returns the index of the current player."
        return self.players.index(self.current_player)
        
    def switch_player(self):
        "Switches the current player."
        curr_idx = self.current_player_index()
        self.current_player = self.players[(curr_idx + 1) % 2]            
            
    def play(self):
        "Play a game of Dog"

        self.field.display()

        # gameplay loop, while the current player has legal moves
        while self.current_player.legal_destinations():
            print('-'*32)
            player = self.current_player
            ms_input = input("{}, enter your move: ".format(player.id))
            
            try:
                ms = process_movestring(ms_input)
                dest = calculate_dest(player, ms)
                
                try:
                    player.move(dest)
                    prev_mover = player  #keep track of who made the last move
                    self.switch_player()
                    self.field.display()
                    
                except IllegalMove:
                    print("That's not a legal move!")
                    
            except InvalidMovestring:
                print("Invalid input!")
            

                

        # at this point, the current player has no legal moves, and the
        # other player wins
    
        loser = self.current_player
        winner = prev_mover
                
        print("!"*10)
        time.sleep(1)
        print("{} is trapped!".format(loser.id))
        time.sleep(1)
        print("{} wins!".format(winner.id))


def process_name(input):
    "Strips whitespace, and returns a random name if the input is empty."
    if not input.strip():
        return random_name()
    else:
        return input.strip()

    
def random_name():
    "Returns a random name from a given input file. Otherwise, returns a default."
    names = open("sample_names.txt").read().splitlines()
    return random.choice(names)


def prompt_for_data():
    """
    Prompts the user for player names and board sizes.
    Cleans up the input and returns it.
    """
    pl1_name_input = input("Player 1, enter your name: ")
    pl1_name = process_name(pl1_name_input)

    pl2_name_input = input("Player 2, enter your name: ")
    pl2_name = process_name(pl2_name_input)

    #rename player 2 if they've chosen the same name as player 1
    if pl2_name == pl1_name:
        pl2_name = random_name()

    # prompt for board size
    size_selected = False
    allowed_size_inputs = [str(i) for i in range(3,16)]

    while size_selected == False:
        size_input = input("Enter board size, between 3 and 15: ")
        if size_input in allowed_size_inputs:
            size_selected = True
        else:
            print("Board size must be an integer between 3 and 15!")

    size = int(size_input)

    return pl1_name, pl2_name, size
       
def play_dog():

    print("~~~~DOG~~~~ (v0.2)")

    pl1_name, pl2_name, size = prompt_for_data()
    game = Game(size, pl1_name, pl2_name)
    game.play()
    

if __name__ == "__main__":
    play_dog()

            

        
