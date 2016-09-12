#!/usr/bin/env python
import sys; sys.path.append("..")
import random
from fireplace import cards
from fireplace.cards.heroes import *
from fireplace.exceptions import GameOver
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft
from fireplace.deck import Deck
from genetic import Genetic
from hearthstone.enums import PlayState

heroes = [WARRIOR, MAGE, PRIEST, SHAMAN, PALADIN, WARLOCK, HUNTER, ROGUE, DRUID]
iterations = 2
pop_count = 2
def main():
	cards.db.initialize()
		
	evo = Genetic(
		iterations=iterations,
		pop_count=pop_count,
		aClass=Evo_Deck,
		aClassParamList=[
		()
		] * pop_count,
		crossoverFunc=crossoverFunction,
		mutationFunc=mutationFunction,
		score_function=scoreFunction,
		goal_func=goalFunction,
		mutation_probability=0.05
	)
	
	final_pop = evo.run()
	for p in final_pop:
		print(p.hero)
		for card in p.deck:
			print(card)
	
def crossoverFunction(A, B):
	#Returns a 'child' of decks A and B, containing components randomly chosen from both.
	cur_deck = A
	new_deck = Evo_Deck()
	i = 0
	while i < len(A.deck) and i < len(B.deck):
		if (random.random() > 0.8):
			if cur_deck == A:
				cur_deck = B
			else:
				cur_deck = A
		new_deck.deck += [cur_deck.deck[i]]
		i += 1
	return new_deck
	
def mutationFunction(A):
	#Return a mutated form of the deck
	i = 0
	new_deck = Evo_Deck()
	while i < len(A.deck):
		if (random.random() > 0.95):
			#Replace the card
			new_card = cards.db[random.choice(list(cards.db.keys()))]
			new_deck.deck += [new_card]
		else:
			new_deck.deck += A.deck[i]
		i += 1
	return new_deck
	
def random_deck():
	return random_draft(hero=random.choice(heroes))
	
def scoreFunction(A):
	print(A)
	#Determine the value of the deck
	return number_wins(A.deck, A.hero)
	
def goalFunction(A):
	#Determine whether the goal has been reached
	#Since we have no predetermined goal for this algorithm, we just return false always
	return False
	
	
def play_full_game(deck1, hero1, deck2, hero2):
	player1 = Player("Player1", deck1, hero1)
	player2 = Player("Player2", deck2, hero2)

	game = Game(players=(player1, player2))
	game.start()

	for player in game.players:
		print("Can mulligan %r" % (player.choice.cards))
		mull_count = random.randint(0, len(player.choice.cards))
		cards_to_mulligan = random.sample(player.choice.cards, mull_count)
		player.choice.choose(*cards_to_mulligan)
	
	while game.players[0].playstate not in (PlayState.LOST, PlayState.WON):
		player = game.current_player

		heropower = player.hero.power
		if heropower.is_usable() and random.random() < 0.1:
			if heropower.has_target():
				heropower.use(target=random.choice(heropower.targets))
			else:
				heropower.use()
			continue

		# iterate over our hand and play whatever is playable
		for card in player.hand:
			if card.is_playable() and random.random() < 0.5:
				target = None
				if card.choose_cards:
					card = random.choice(card.choose_cards)
				if card.has_target():
					target = random.choice(card.targets)
				print("Playing %r on %r" % (card, target))
				card.play(target=target)

				if player.choice:
					choice = random.choice(player.choice.cards)
					print("Choosing card %r" % (choice))
					player.choice.choose(choice)

				continue

		# Randomly attack with whatever can attack
		for character in player.characters:
			if character.can_attack():
				character.attack(random.choice(character.targets))
			continue

		game.end_turn()
	
	return Game.players[0].playstate == PlayState.WON
	


def number_wins(deck, player_hero):
	opponents = [(WARRIOR, random_draft(hero=WARRIOR))]
	wins = 0
	for opponent_hero, opponent_deck in opponents:
		try:
			wins += 1 if play_full_game(deck, player_hero, opponent_deck, opponent_hero) else 0
		except GameOver:
			print("Game completed normally.")
		except:
			print("Game did not finish successfully - there must be an error somewhere")
			return 0
	return wins

class Evo_Deck:
	def __init__(self):
		#Randomly generate myself
		self.hero = random.choice(heroes)
		self.deck = random_draft(hero=self.hero)

if __name__ == "__main__":
	main()