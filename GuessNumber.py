import simplegui
import random
import math

def new_game(range):
    """
    This function uses input to start a new game
    
    :input n: integer that is used to determine secret number high range and the
              number of guesses for a game
    """
    global secret_number
    global counter
    global n
    n = range
    
    secret_number = random.randrange(0, n)
    counter = int(math.ceil(math.log(n + 1)/math.log(2)))
    
    print "New Game. Range is from 0 to", n
    print "Number of remaining guesses is",counter
    print ""

def range100():
    # button that changes the range to [0,100) and starts a new game 
    new_game(100)

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    new_game(1000)
    
    
def input_guess(guess):
    """
    Calculates number of remaining guesses and contains logic that determines
    if the guess was lower, higher or correct. Also determines if game is over, 
    if so, it will start a new game
    """
    global counter
    global secret_number
    
    guess_int = int(guess)
    counter = counter - 1
    
    print "Guess was", guess_int
    if guess_int == secret_number:
        print "Correct!"
        print ""
        new_game(n)
        return
    elif guess_int > secret_number and counter != 0:
        print "Number of remaining guesses is", counter
        print "Lower!"
        print ""
    elif guess_int < secret_number and counter != 0:
        print "Number of remaining guesses is", counter
        print "Higher!"
        print ""
    else:
        print "You ran out of guesses. The number was",secret_number
        print ""
        new_game(n)
        
# Create frame and event handlers
frame = simplegui.create_frame("Guess the Number!", 200, 200)

# Control Elements
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter Guess", input_guess, 200)
frame.start()

# Call new_game, defaults to 100 high range 
new_game(100)

