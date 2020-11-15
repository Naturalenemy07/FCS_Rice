# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0,0]

padL_pos = [0, (HEIGHT - PAD_HEIGHT)/2]
padR_pos = [WIDTH - PAD_WIDTH, (HEIGHT - PAD_HEIGHT)/2]
padL_vel = [0,0]
padR_vel = [0,0]

scoreL = 0
scoreR = 0
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    x_rand = random.randrange(120, 240) / 60
    y_rand = random.randrange(60, 240) / 60
    
    if direction == RIGHT:
        ball_vel = [x_rand, -y_rand]
    elif direction == LEFT:
        ball_vel = [-x_rand, -y_rand]

# define event handlers
def new_game():
    global padL_pos, padR_pos, padL_vel, padR_vel  # these are numbers
    global scoreL, scoreR  # these are ints
    scoreL = 0
    scoreR = 0
    padL_pos = [0, (HEIGHT - PAD_HEIGHT)/2]
    padR_pos = [WIDTH - PAD_WIDTH, (HEIGHT - PAD_HEIGHT)/2]
    padL_vel = [0,0]
    padR_vel = [0,0]
    
    spawn_ball(RIGHT)

def draw(canvas):
    global scoreL, scoreR, padL_pos, padR_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = ball_vel[1] * -1
        
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= padL_pos[1] and ball_pos[1] <= padL_pos[1] + PAD_HEIGHT:
            ball_vel[0] = ball_vel[0] * -1.1
        else:
            scoreR += 1
            spawn_ball(RIGHT)
    
    if ball_pos[0] + BALL_RADIUS > WIDTH - PAD_WIDTH:
        if ball_pos[1] >= padR_pos[1] and ball_pos[1] <= padR_pos[1] + PAD_HEIGHT:
            ball_vel[0] = ball_vel[0] * -1.1
        else:
            scoreL += 1
            spawn_ball(LEFT)
      
    
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'white','white')
    
    # update paddle's vertical position, keep paddle on the screen
    if padL_pos[1] + padL_vel[1] < 0 or padL_pos[1] + PAD_HEIGHT + padL_vel[1] > HEIGHT:
        padL_vel[1] = 0
    elif padR_pos[1] + padR_vel[1] < 0 or padR_pos[1] + PAD_HEIGHT + padR_vel[1] > HEIGHT:
        padR_vel[1] = 0

    padL_pos[1] += padL_vel[1]
    padR_pos[1] += padR_vel[1]
    
    # draw paddles
    canvas.draw_polygon([[padL_pos[0],padL_pos[1]], [padL_pos[0],padL_pos[1]+PAD_HEIGHT], [padL_pos[0]+PAD_WIDTH,padL_pos[1]+PAD_HEIGHT], [padL_pos[0]+PAD_WIDTH,padL_pos[1]]], 1, 'White', 'White')
    canvas.draw_polygon([[padR_pos[0],padR_pos[1]], [padR_pos[0],padR_pos[1]+PAD_HEIGHT], [padR_pos[0]+PAD_WIDTH,padR_pos[1]+PAD_HEIGHT], [padR_pos[0]+PAD_WIDTH,padR_pos[1]]], 1, 'White', 'White')
    
    # draw scores
    canvas.draw_text(str(scoreL),[140,50], 50, 'white')
    canvas.draw_text(str(scoreR),[436,50], 50, 'white')
        
def keydown(key):
    global padL_vel, padR_vel
    if key == simplegui.KEY_MAP['w']:
        padL_vel[1] = -3
    elif key == simplegui.KEY_MAP['s']:
        padL_vel[1] = 3
    elif key == simplegui.KEY_MAP['up']:
        padR_vel[1] = -3
    elif key == simplegui.KEY_MAP['down']:
        padR_vel[1] = 3
   
def keyup(key):
    global padL_vel, padR_vel
    if key == simplegui.KEY_MAP['w']:
        padL_vel[1] = 0
    elif key == simplegui.KEY_MAP['s']:
        padL_vel[1] = 0
    elif key == simplegui.KEY_MAP['up']:
        padR_vel[1] = 0
    elif key == simplegui.KEY_MAP['down']:
        padR_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
