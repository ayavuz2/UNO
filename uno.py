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
BLACK_CARD_TYPES = ['wildcard', '+4']
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES


class Card():
	def __init__(self, color, card_type):
		self.color = color
		self.card_type = card_type
		self.png = pygame.image.load(os.path.join("images", "{}_{}".format(color, card_type)))


def draw(win):
	win.fill((255,255,255))

	pygame.display.update()


def main():
	run = True
	FPS = 15

	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)
		draw(WIN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


main()
