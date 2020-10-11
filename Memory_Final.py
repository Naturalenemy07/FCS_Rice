# implementation of card game - Memory

import simplegui
import random

cardlist = list(range(0,8))
cardlist_copy = list(range(0,8))
cardlist.extend(cardlist_copy)
exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
state = 0
random.shuffle(cardlist)

CARD_WIDTH = 50
CARD_HEIGHT = 100
CARD_FILL = 'RGBA(34, 49, 63, 1)'
CARD_EDGE = 'RGBA(228, 241, 254, 1)'
CARDS_PER_ROW = 8
TOTAL_ROWS = 2
card1value = 0
card2value = 0
counter = 0
turn_counter = "Turn: 0"

# helper function to initialize globals
def new_game():
    global counter
    global turn_counter
    global cardlist
    global exposed
    global state
    global card1value
    global card2value
    
    counter = 0
    turn_counter = "Turn: 0"
    random.shuffle(cardlist)
    for i in range(0, len(exposed)):
        exposed[i] = False
    state = 0
    card1value = 0
    card2value = 0
    
    label.set_text(turn_counter)
    

# define event handlers
def mouseclick(pos):
    global exposed
    global state
    global card1value
    global card2value
    global counter
    global turn_counter
    
    
    
    for i in range(0, CARDS_PER_ROW):
        for j in range(0, TOTAL_ROWS):
            if pos[0] > i*CARD_WIDTH and pos[0] < (i+1)*CARD_WIDTH:
                if pos[1] > j*CARD_HEIGHT and pos[1] < CARD_HEIGHT*(j+1):
                    
                    #first row of cards
                    if j == 0:    
                        
                        #checks/changes the state if the card clicked is not exposed 
                        if exposed[i] == False:
                            if state == 0:
                                state = 1
                                counter += 1
                                card1value = cardlist[i]
                            elif state == 1:
                                state = 2
                                #counter += 1
                                card2value = cardlist[i]
                            elif state == 2:
                                if card1value != card2value:
                                    for c in range(0, len(cardlist)):
                                        if cardlist[c] == card1value:
                                            exposed[c] = False
                                        if cardlist[c] == card2value:
                                            exposed[c] = False
                                    counter += 1
                                    card1value = cardlist[i]
                                    state = 1
                                elif card1value == card2value:
                                    state = 1
                                    counter += 1
                                    card1value = cardlist[i]
                            exposed[i] = True
                    
                    #second row of cards, currently not working
                    elif j == 1:
                        
                        #checks/changes the state if the card clicked is not exposed 
                        if exposed[CARDS_PER_ROW + i] == False:
                            if state == 0:
                                state = 1
                                counter += 1
                                card1value = cardlist[CARDS_PER_ROW + i]
                            elif state == 1:
                                state = 2
                                #counter += 1
                                card2value = cardlist[CARDS_PER_ROW + i]
                            elif state == 2:
                                if card1value != card2value:
                                    for c in range(0, len(cardlist)):
                                        if cardlist[c] == card1value:
                                            exposed[c] = False
                                        if cardlist[c] == card2value:
                                            exposed[c] = False
                                    counter += 1
                                    card1value = cardlist[CARDS_PER_ROW + i]
                                    state = 1
                                elif card1value == card2value:
                                    state = 1
                                    counter += 1
                                    card1value = cardlist[CARDS_PER_ROW + i]
                            exposed[CARDS_PER_ROW + i] = True
    turn_counter = "Turn: " + str(counter)
    label.set_text(turn_counter)
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(0, CARDS_PER_ROW):
        for j in range(0, TOTAL_ROWS):
            canvas.draw_polygon([(i*CARD_WIDTH, j*CARD_HEIGHT), (i*CARD_WIDTH, CARD_HEIGHT*(j+1)), ((i+1)*CARD_WIDTH, CARD_HEIGHT*(j+1)), ((i+1)*CARD_WIDTH, j*CARD_HEIGHT)], 2, CARD_EDGE, CARD_FILL)
            if j == 0:
                if exposed[i] == True:
                    canvas.draw_text(str(cardlist[i]), (i*CARD_WIDTH+(CARD_WIDTH*0.3), CARD_HEIGHT*(j+1)-(CARD_HEIGHT*0.4)), 40, 'White')
            elif j == 1:
                if exposed[CARDS_PER_ROW + i] == True:
                    canvas.draw_text(str(cardlist[CARDS_PER_ROW + i]), (i*CARD_WIDTH+(CARD_WIDTH*0.3), CARD_HEIGHT*(j+1)-(CARD_HEIGHT*0.4)), 40, 'White')
                

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 400, 200)
frame.add_button("Reset", new_game)
label = frame.add_label("Turn: 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
