import pygame
import os
# import sys
import random
pygame.font.init()


WIDTH, HEIGHT = 775, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO")

COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(10)) + list(range(1,10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES*2
BLACK_CARD_TYPES = ['wildcard', '+4']*4
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES
CARD_WIDTH, CARD_HEIGHT = 72, 108

# Creating a deck
def create_deck(deck):

	def return_shuffled(color_card_types):
		random.shuffle(color_card_types)
		return color_card_types

	for color in COLORS:
		deck[color] = return_shuffled(COLOR_CARD_TYPES[:])

	return_shuffled(COLOR_CARD_TYPES[:])
	deck['black'] = BLACK_CARD_TYPES
	# print(sys.getsizeof(deck))


class Card():
	def __init__(self, color, card_type):
		self.color = color
		self.card_type = card_type
		self.png = pygame.image.load(os.path.join("images", "{}_{}.png".format(self.color, self.card_type))) # green_.png

	def __eq__(self, other):
		return self.color == other.color or self.card_type == other.card_type or self.color == 'black'

	def render_card(self, win, x, y, gap, change_row):		
		win.blit(self.png, (x, y - (CARD_HEIGHT+gap)*change_row)) # update it with flexible heights
		# win.blit(self.png, (x%WIDTH, y-(CARD_HEIGHT+gap)))


class Mid(Card):
	def __init__(self, color, card_type):
		super().__init__(color, card_type)
		self.x = WIDTH//2 - CARD_WIDTH//2
		self.y = HEIGHT//2 - CARD_HEIGHT//2

	def render_card(self, win):
		win.blit(self.png, (self.x, self.y))

	def __eq__(self, other):
		return self.color == other.color or self.card_type == other.card_type or self.color == 'black'


class Player():
	def __init__(self, name):
		self.name = name
		self.player_cards = []

	def draw_a_card_from_deck(self, deck):		
		self.player_cards.append(draw_a_card(deck))

	def set_initial_cards(self, deck):
		for i in range(15):
			self.draw_a_card_from_deck(deck) 
		'''for card in self.player_cards:
			print(card.color, card.card_type, end='  ---   ')'''

	def get_len(self):
		return len(self.player_cards)

	def is_finished(self):
		return len(self.player_cards) == 0

	def is_playable(self, card_index, middle_card):
		pass

	def render_players_cards(self, win, width, height, gap): # it is kinda complex :)		
		total_gap = gap
		row_change_point = get_max_horizontal(width, gap)
		total_row = self.get_len()//row_change_point if self.get_len()%row_change_point == 0 else self.get_len()//row_change_point + 1  
		check = 0

		for card in self.player_cards: # try [:] 
			if check == row_change_point:
				total_row -= 1
				check = 0 
				total_gap = gap
			card.render_card(win, total_gap, height, gap, total_row) # make (x, y) flexible for render_card function
			total_gap += (CARD_WIDTH + gap)
			check += 1


def draw_a_card(deck, is_mid=False):
	colors = list(deck.keys())

	# Adding probability to the colors depending on how many cards they do have
	weights = []
	for clr in colors:
		weights.append(len(deck[clr]))
	color = random.choices(colors, weights=weights, k=1) # k is the number of choosing
	color = ''.join(color) # list to string

	card = Card(color, deck[color].pop()) if is_mid == False else Mid(color, deck[color].pop())

	return card


def get_number_of_rows(width, gap, number_of_cards):
	return (number_of_cards*CARD_WIDTH + (number_of_cards+1)*gap)//width + 1

def get_max_horizontal(width, gap):
	max_horizontal_cards = 1
	while ((gap+CARD_WIDTH)*max_horizontal_cards)//width < 1:
		max_horizontal_cards += 1
	return max_horizontal_cards

def get_click_pos(pos, width, height, gap, number_of_cards): # work in progress...
	x, y = pos
	number_of_rows = get_number_of_rows(width, gap, number_of_cards)
	
	# checking if the cursor is in a specific area and also not on the gaps
	area_height = number_of_rows*CARD_HEIGHT + (number_of_rows+1)*gap # height of the area
	if y>height-area_height and (height-y) % (CARD_HEIGHT+gap) >= gap:
		row = (area_height - (height-y))//(CARD_HEIGHT+gap)
		if x % (CARD_WIDTH+gap) >= gap:
			col = x//(CARD_WIDTH+gap) 
			return row, col # works fine but the render is not matching with the virtual row and col rn. Fix the render!

	return None, None

def draw(win, width, height, player, gap, mid):
	win.fill((255,255,255))

	mid.render_card(win)

	player.render_players_cards(win, width, height, gap)

	pygame.display.update()


def main(win, width, height):
	run = True
	FPS = 30
	clock = pygame.time.Clock()

	DECK = dict()
	create_deck(DECK)
	
	MID_CARD = []
	MID_CARD.append(draw_a_card(DECK, True))
	GAP = 5

	player = Player('Tom')
	player.set_initial_cards(DECK)

	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			# print(pos)
			row, col = get_click_pos(pos, width, height, GAP, player.get_len())
			print(row, col)

		if pygame.mouse.get_pressed()[2]: # Changing card positions
			pass 

		draw(win, width, height, player, GAP, MID_CARD[0])

main(WIN, WIDTH, HEIGHT)
