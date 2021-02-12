class IllegalMove(Exception):
    "Exception raised when a proposed move is illegal."


def distance(pt1, pt2):
    """
    Gives the (Manhattan) distance between two points
    pt1 (Int, Int), pt2 (Int, Int)
    """
    return abs(pt1[0] - pt2[0]) + abs(pt2[1] - pt2[1])


class Player:
    """
    Represents a player.
    """
    def __init__(self, field, id, position):
        assert len(field.players) < 2, 'Field can contain maximum 2 players'
        self.field = field
        self.id = id

        assert position in field.points, (
            'Player position must be on the playfield')
        self.position = position

        self.field.players.append(self)

    def legal_destinations(self):
        "Set of all points in the playfield to which the player can move."
        return {pt for pt in self.field.points if is_legal(self, pt)}

    def has_legal_moves(self):
        "True if the player has legal moves, False otherwise"
        return bool(self.current_player.legal_destinations()):

    def place(self, dest):  # should use setters + getters here...
        """
        Place the player on the board.
        """
        self.position = dest


class Move:
    """
    class representing a (possibly invalid or illegal) move
    """
    def __init__(self, player, dest):
        """
        player (Player): player to be moved
        dest (Int, Int): destination of proposed move
        """
        self.player = player
        self.dest = dest

    def is_legal(self):
        """
        test whether the move is legal
        """
        if not dest in player.field.points:
            return False

        if player.field.is_occupied(dest):
            return False

        if not 1 <= distance(self.player.position, self.player.dest) <= 2:
            return False

        return True

    def execute(self):
        """
        execute the move, if legal
        """

        if self.is_legal():
            old_position = self.player.position
            self.player.place(dest)
            self.field.remove(old_position)
        else:
            raise IllegalMove


class Playfield:
    """
    The field of play. Initialises as a square of specified sidelength
    (default 10)
    """
    def __init__(self, size=10):
        self.size = size
        self.points = {(x, y) for x in range(size) for y in range(size)}
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
        """
        assert self.contains(point), (
            'Specified point not contained in playfield')
        self.points.remove(point)


class Game:
    "A game of Dog."
    def __init__(self, size, player1, player2):
        """
        size (Int): size of the playfield
        player1 (Player)
        player2 (Player)
        """

        self.field = Playfield(size)
        self.players = [p1, p2]

        self.player1.place((0,0))
        self.player2.place((size-1,size-1))

        # set a random starting player
        self.current_player = random.choice(self.players)

    def current_player_index(self):
        "Returns the index of the current player."
        return self.players.index(self.current_player)

    def switch_player(self):
        "Switches the current player."
        curr_idx = self.current_player_index()
        self.current_player = self.players[(curr_idx + 1) % 2]
