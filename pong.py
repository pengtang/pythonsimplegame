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
ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos = [[0, 0], [0, 0], [0, 0], [0, 0]]
paddle2_pos = [[0, 0], [0, 0], [0, 0], [0, 0]]
paddle1_vel = 0
paddle2_vel = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2
    if direction == "RIGHT":
        ball_vel[0] = 2 * random.random() + 2
        ball_vel[1] = (random.random()-0.5) * 8
    else:
        ball_vel[0] = -2 * random.random() - 2
        ball_vel[1] = (random.random()-0.5) * 8
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(1)
    score1 = 0
    score2 = 0
    paddle1_pos = [[0, (HEIGHT-PAD_HEIGHT)/2], [PAD_WIDTH, (HEIGHT-PAD_HEIGHT)/2], [PAD_WIDTH, HEIGHT-(HEIGHT-PAD_HEIGHT)/2], [0, HEIGHT-(HEIGHT-PAD_HEIGHT)/2]]
    paddle2_pos = [[WIDTH-PAD_WIDTH, (HEIGHT-PAD_HEIGHT)/2], [WIDTH, (HEIGHT-PAD_HEIGHT)/2], [WIDTH, HEIGHT-(HEIGHT-PAD_HEIGHT)/2], [WIDTH-PAD_WIDTH, HEIGHT-(HEIGHT-PAD_HEIGHT)/2]]
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel     
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "Blue")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[0][1] + paddle1_vel>=0) and (paddle1_pos[2][1] + paddle1_vel<=HEIGHT):
        for pos in paddle1_pos:
            pos[1] += paddle1_vel
    elif paddle1_pos[0][1] + paddle1_vel<0:
        paddle1_pos[0][1] = 0
        paddle1_pos[1][1] = 0        
        paddle1_pos[2][1] = PAD_HEIGHT  
        paddle1_pos[3][1] = PAD_HEIGHT          
    elif paddle1_pos[2][1] + paddle1_vel>HEIGHT:
        paddle1_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle1_pos[1][1] = HEIGHT - PAD_HEIGHT     
        paddle1_pos[2][1] = HEIGHT  
        paddle1_pos[3][1] = HEIGHT
        
    if (paddle2_pos[0][1] + paddle2_vel>=0) and (paddle2_pos[2][1] + paddle2_vel<=HEIGHT):
        for pos in paddle2_pos:
            pos[1] += paddle2_vel    
    elif paddle2_pos[0][1] + paddle2_vel<0:
        paddle2_pos[0][1] = 0
        paddle2_pos[1][1] = 0        
        paddle2_pos[2][1] = PAD_HEIGHT  
        paddle2_pos[3][1] = PAD_HEIGHT          
    elif paddle1_pos[2][1] + paddle1_vel>HEIGHT:
        paddle2_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle2_pos[1][1] = HEIGHT - PAD_HEIGHT     
        paddle2_pos[2][1] = HEIGHT  
        paddle2_pos[3][1] = HEIGHT    
        
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'Green', "White")
    canvas.draw_polygon(paddle2_pos, 1, 'Green', "White")
    
    # determine whether paddle and ball collide    
    # upper bound
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] *= -1
    # lower bound
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] *= -1
    # left bound
    if ball_pos[0] - BALL_RADIUS - PAD_WIDTH <= 0:
        if ball_pos[1]<=paddle1_pos[2][1] and ball_pos[1]>=paddle1_pos[0][1]:
            ball_vel[0] *= -1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    # right bound
    if ball_pos[0] + BALL_RADIUS + PAD_WIDTH >= WIDTH:
        if ball_pos[1]<=paddle2_pos[2][1] and ball_pos[1]>=paddle2_pos[0][1]:
            ball_vel[0] *= -1.1
        else:
            score1 += 1
            spawn_ball(LEFT)    
    # draw scores
    canvas.draw_text("Player 1 scores: " + str(score1), [100, 20], 20, "green")
    canvas.draw_text("Player 2 scores: " + str(score2), [400, 20], 20, "green")
def keydown(key):
    global paddle1_vel, paddle2_vel
    current_key = chr(key)
    if current_key == "&":
        paddle2_vel = -4
    elif current_key == "(":
        paddle2_vel = 4
    
    if current_key == "W":
        paddle1_vel = -4
    elif current_key == "S":
        paddle1_vel = 4

def keyup(key):
    global paddle1_vel, paddle2_vel
    current_key = chr(key)
    if current_key == "&":
        paddle2_vel = 0
    elif current_key == "(":
        paddle2_vel = 0
    
    if current_key == "W":
        paddle1_vel = 0
    elif current_key == "S":
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
