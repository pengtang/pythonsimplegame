# Game Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
is_stand = False
outcome = ""
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = "Hand contains "
        for card in self.cards:
            s += str(card)
        return s

    def add_card(self, card):
        self.cards.append(card)

    def get_card(self, index):
        index -= 1
        return self.cards[index]
    
    def get_value(self):
        s = 0
        has_ace = False
        for card in self.cards:
            if card.get_rank()!="A":
                s += VALUES[card.get_rank()]
            elif has_ace == False and s+11<=21:
                s += VALUES[card.get_rank()] + 10
                has_ace = True
            else:
                s += VALUES[card.get_rank()]
        return s
    
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards: 
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.suit))        	
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + i*80 + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            i += 1
     
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s,r))

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        s = "Deck contains "
        for card in self.cards:
            s += str(card)
        return s

# start a new game, and initialize.
def deal():
    global outcome, in_play, is_stand, player, dealer, deck	
    # initialization
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    outcome = ""
    
    # player adds two cards
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    # dealer adds two cards with one now shown
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    in_play = True
    is_stand = False

def hit():
    # if the hand is in play, hit the player
    global player, player_score, outcome, in_play
    if in_play:
        player.add_card(deck.deal_card())
        player_score = player.get_value()
        if player_score>21:
            outcome = "Dealer wins"
            player_score = player.get_value()
            in_play = False
    # if busted, assign a message to outcome, update in_play and score

def stand():
    global dealer, dealer_score, player_socre, outcome, in_play, is_stand
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    is_stand = True
    while in_play:
        dealer_score = dealer.get_value()
        if dealer_score>=17:
            if dealer_score>=player_score and dealer_score<=21:
                outcome = "Dealer wins"
            else:
                outcome = "Player wins"
            in_play = False
        else:
            dealer.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer, outcome
    player.draw(canvas, [150, 300])
    #dealer.draw(canvas, [450, 150])
    # do not draw the first card if player is still playing
    if not is_stand: 
        card_back_pos = [150, 150]
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [card_back_pos[0] + CARD_BACK_CENTER[0], card_back_pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        temp_card = dealer.get_card(2)
        temp_card.draw(canvas, [150 + 80, 150])
    else:
        dealer.draw(canvas, [150, 150])
    canvas.draw_text(outcome, [350,50], 20, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
