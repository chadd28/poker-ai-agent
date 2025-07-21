import random

SUITS = ['h','d','c','s']
RANKS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

def deal_hole_cards():
    deck = [r + s for r in RANKS for s in SUITS]
    return [random.sample(deck, 2)]


def deal_community_cards(num_cards):
    deck = [r + s for r in RANKS for s in SUITS]
    return random.sample(deck, num_cards)
