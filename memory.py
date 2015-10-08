# implementation of card game - Memory

import simplegui
import random


# helper function to initialize globals
counter = 0
cards = []
exposure = []
exp_sum = 0
exp_num = []
exp_pos = []
def new_game():
    global counter, cards, exposure, exp_sum, exp_num, exp_pos
    # initialize cards number
    counter = 0
    arr = [1,2,3,4,5,6,7,8]
    arr.extend(arr)
    random.shuffle(arr)
    cards = list(arr)
    # initialize the cards exposure
    exposure = []
    for i in range(16):
        exposure.append(False)
    exp_sum = 0
    exp_num = []
    exp_pos = []
    label.set_text("Turns = " + str(counter))
     
# define event handlers
def mouseclick(pos):
    global counter, cards, exposure, exp_sum, exp_num, exp_pos
    if pos[0]<800 and pos[0]>0 and pos[1]<100 and pos[1]>0:
        click_pos = pos[0]//50
        # effective click

        if (not exposure[click_pos]):
            #	empty
            if exp_sum == 0:
                counter += 1
                exposure[click_pos] = True
                exp_num.append(cards[click_pos])
                exp_pos.append(click_pos)
                exp_sum += 1
            elif exp_sum == 1:
                counter += 1
                exposure[click_pos] = True
                # Match?
                if cards[click_pos] == exp_num[0]:
                    exp_sum = 0
                    exp_num = []
                    exp_pos = []
                else:
                    exp_sum += 1
                    exp_num.append(cards[click_pos])
                    exp_pos.append(click_pos)
            else:
                # cover that not matched pair
                for i in exp_pos:
                    exposure[i] = False
                exp_sum = 0
                exp_num = []
            label.set_text("Turns = " + str(counter))

# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposure[i]:
            canvas.draw_polygon([[i*50,0],[(i+1)*50,0],[(i+1)*50,100],[i*50,100]],1,"white","red")
            canvas.draw_text(str(cards[i]), [i*50 + 17, 55], 40, "White")
        else:
            canvas.draw_polygon([[i*50,0],[(i+1)*50,0],[(i+1)*50,100],[i*50,100]],1,"white","green")
            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

