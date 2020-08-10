import pygame
import os
from time import sleep
import random
pygame.font.init()


WIDTH, HEIGHT = 775, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO")

FONT = pygame.font.SysFont("comicsans", 50)

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


class Card:
	def __init__(self, color, card_type=''):
		self.color = color
		self.card_type = card_type
		self.png = pygame.image.load(os.path.join("images", "{}_{}.png".format(self.color, self.card_type)))

	def render_card(self, win, x, y, gap, change_row):		
		win.blit(self.png, (x, y - (CARD_HEIGHT+gap)*change_row))


class Mid(Card):
	def __init__(self, color, card_type):
		super().__init__(color, card_type)
		self.x = WIDTH//2 - CARD_WIDTH//2
		self.y = HEIGHT//2 - CARD_HEIGHT//2

	def render_card(self, win):
		win.blit(self.png, (self.x, self.y))


class Player:
	def __init__(self, name):
		self.name = name
		self.player_cards = []

	def move(self, width, row, col, middle_card, gap, deck):
		card_index = get_card_index(width, gap, row, col)
		
		if self.get_len() == card_index+1: # draw_a_card slot
			sleep(0.1)
			self.draw_a_card_from_deck(deck)
			tmp = self.player_cards.pop(-2)
			self.player_cards.append(tmp)

		elif self.is_playable(card_index, middle_card):
			sleep(0.1) # trying to prevent the user's unintentional card choosings back to back
			new_mid = self.player_cards.pop(card_index)
			new_mid = Mid(new_mid.color, new_mid.card_type)		
			return(new_mid)

		else:
			print("That move is not allowed!")	

	def draw_a_card_from_deck(self, deck):		
		self.player_cards.append(draw_a_card(deck))

	def set_initial_cards(self, deck):
		for i in range(7):
			self.draw_a_card_from_deck(deck) 
		draw_card_slot = Card('back')
		self.player_cards.append(draw_card_slot)

	def get_len(self):
		return len(self.player_cards)

	def is_finished(self):
		return len(self.player_cards) == 1 # draw_a_card slot is not actually a card so that is where 1 comes from

	def is_playable(self, card_index, middle_card):
		tmp = self.player_cards[card_index]
		if tmp.color == middle_card.color or tmp.card_type == middle_card.card_type or tmp.color == 'black':
			return True
		if tmp.card_type == '+2' and middle_card.card_type == '+4': # +4 will make the user choose a color so this will be unnecessary
			return True
		return False

	def render_players_cards(self, win, width, height, gap):		
		row_change_point = get_max_horizontal(width, gap) # Make a global var MAX_HORIZONTAL which will be calculated at the beginning
		number_of_rows = get_number_of_rows(width, gap, self.get_len())
		total_gap = gap
		check = 1

		for i in range(number_of_rows, 0, -1):
			total_gap = gap
			while check % row_change_point != 0 and check-1 != self.get_len():
				self.player_cards[check-1].render_card(win, total_gap, height, gap, i)
				total_gap += (CARD_WIDTH + gap)
				check += 1
			if check-1 != self.get_len():
				self.player_cards[check-1].render_card(win, total_gap, height, gap, i)
			check += 1


def draw_a_card(deck, is_mid=False):
	colors = list(deck.keys())

	# Adding probability to the colors depending on how many cards they do have
	weights = []
	for clr in colors:
		weights.append(len(deck[clr]))
	color = random.choices(colors, weights=weights, k=1) # k is the number of choosing
	color = ''.join(color) # list to string

	card = Card(color, deck[color].pop()) if not is_mid else Mid(color, deck[color].pop()) # Mid color shouldnt be black at the beginning

	return card


def get_number_of_rows(width, gap, number_of_cards):
	return (number_of_cards*CARD_WIDTH + (number_of_cards+1)*gap)//width + 1

def get_max_horizontal(width, gap):
	max_horizontal_cards = 1
	while ((gap+CARD_WIDTH)*max_horizontal_cards)//width < 1:
		max_horizontal_cards += 1
	return max_horizontal_cards - 1 

def get_card_index(width, gap, row, col):
	max_in_a_row = get_max_horizontal(width, gap)
	return((row * max_in_a_row + (col+1)) - 1)

def get_click_pos(pos, width, height, gap, number_of_cards):
	x, y = pos
	number_of_rows = get_number_of_rows(width, gap, number_of_cards)
	
	# checking if the cursor is in a specific area and also not on the gaps
	area_height = number_of_rows*CARD_HEIGHT + (number_of_rows+1)*gap # height of the area
	if y>height-area_height and (height-y) % (CARD_HEIGHT+gap) >= gap:
		row = (area_height - (height-y))//(CARD_HEIGHT+gap)
		if x % (CARD_WIDTH+gap) >= gap:
			col = x//(CARD_WIDTH+gap) 
			return row, col

	return None, None

def pass_button_area(width, height, message):
	message_label = FONT.render(message, 1, (255,0,0))

	w, h = message_label.get_width(), message_label.get_height()
	rect_area = (width//2 + CARD_WIDTH*2 - 10, height//2 - h//2 -10, w+20, h+20)

	return rect_area

def render_message(win, width, height, message):
	message_label = FONT.render(message, 1, (255,0,0))

	pygame.draw.rect(win, (190,190,190), pass_button_area(width, height, message))

	win.blit(message_label, (width//2 + CARD_WIDTH*2, height//2 - message_label.get_height()//2))

def draw(win, width, height, player, gap, mid, message='PASS'):
	win.fill((255,255,255))

	mid.render_card(win)
	player.render_players_cards(win, width, height, gap)

	render_message(win, width, height, message)

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
	
	pass_button = pass_button_area(width, height, "PASS")

	'''
	players = []
	for name in ['Tom', 'Alex', 'Jason', 'Anders']:
		player = Player(name)
		player.set_initial_cards(DECK)
		players.append(player)
	'''
	player = Player('Tom')
	player.set_initial_cards(DECK)

	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			

			row, col = get_click_pos(pos, width, height, GAP, player.get_len())

			try:
				if row != None:
					tmp = player.move(width, row, col, MID_CARD[0], GAP, DECK)
					if tmp != None:
						MID_CARD[0] = tmp
			except IndexError:
				continue

			if pass_button[0] < pos[0] and pass_button[1] < pos[1] and pos[0] < pass_button[0]+pass_button[2] and pos[1] < pass_button[1]+pass_button[3]:
				print(True)
				sleep(0.1)

		if pygame.mouse.get_pressed()[2]: # Changing card positions
			pass 

		draw(win, width, height, player, GAP, MID_CARD[0])

main(WIN, WIDTH, HEIGHT)
