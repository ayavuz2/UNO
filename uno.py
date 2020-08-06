import pygame
import os
import random
pygame.font.init()


WIDTH, HEIGHT = 600, 600
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


class Card():
	def __init__(self, color, card_type):
		self.color = color
		self.card_type = card_type
		self.png = None

	def __eq__(self, other):
		return self.color == other.color and self.card_type == other.card_type

	def draw_card(self):
		self.png = pygame.image.load(os.path.join("images", "{}_{}".format(self.color, self.card_type)))
		# draw...


class Player():
	def __init__(self, name):
		self.name = name
		self.player_cards = []

	def draw_a_card_from_deck(self, card):
		self.player_cards.append(card)

	def set_initial_cards(self, deck):
		for i in range(7):
			self.player_cards.append()

	def is_finished(self):
		return len(self.player_cards) == 0

	def is_playable(self, card_index, middle_card):
		pass


def draw(win):
	win.fill((255,255,255))

	pygame.display.update()


def main():
	run = True
	FPS = 15

	DECK = dict()
	clock = pygame.time.Clock()

	create_deck(DECK)
	# tmp = random.choice(list(DECK.keys()))
	# print(tmp, (DECK[tmp].pop()))

	while run:
		clock.tick(FPS)
		draw(WIN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


main()
