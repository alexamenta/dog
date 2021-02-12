# functions dealing with move strings (text input for move)
import re       # used in processing movestrings
import random   # used in generating random names


class InvalidMovestring(Exception):
    "Exception raised when a given movestring is invalid."


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


# formerly a method of Game

def prompt_for_move(self):
    """
    Prompts the current player for a move.
    """
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

# UI stuff to be modified later

def process_name(input):
    "Strips whitespace, and returns a random name if the input is empty."
    if not input.strip():
        return random_name()

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

