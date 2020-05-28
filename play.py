from main import *

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
