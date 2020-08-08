import pygame
import os
import sys
import random
pygame.font.init()


WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO")

COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(10)) + list(range(1,10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES*2
BLACK_CARD_TYPES = ['wildcard', '+4']*4
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES

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
		self.png = pygame.image.load(os.path.join("images", "{}_{}.png".format(self.color, self.card_type)))

	def __eq__(self, other):
		return self.color == other.color and self.card_type == other.card_type

	def draw_card(self, win, width, height, gap):		
		win.blit(self.png, (gap, height-150))


class Player():
	def __init__(self, name):
		self.name = name
		self.player_cards = []

	def draw_a_card_from_deck(self, deck):
		colors = list(deck.keys())
		weights = []

		for clr in colors:
			weights.append(len(deck[clr]))

		print(weights)
		color = random.choices(colors, weights=weights, k=1) # k is the number of choosing
		color = ''.join(color) # list to string

		card = Card(color, deck[color].pop())
		self.player_cards.append(card)

	def set_initial_cards(self, deck):
		for i in range(7):
			self.draw_a_card_from_deck(deck) 

	def is_finished(self):
		return len(self.player_cards) == 0

	def is_playable(self, card_index, middle_card):
		pass

	def draw_players_cards(self, win, width, height):
		gap = 10
		for card in self.player_cards: # try [:] 
			card.draw_card(win, width+0, height, gap)
			gap += 80


def get_click_pos(pos): # work in progress...
	print(pos)

def draw(win, width, height, player):
	win.fill((255,255,255))

	player.draw_players_cards(win, width, height)

	pygame.display.update()


def main(win):
	run = True
	FPS = 15

	DECK = dict()
	clock = pygame.time.Clock()

	create_deck(DECK)

	player = Player('Tom')
	player.set_initial_cards(DECK)
	

	# print("*********************")
	# print(DECK)

	while run:
		clock.tick(FPS)
		draw(win, WIDTH, HEIGHT, player)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			get_click_pos(pos)


main(WIN)
