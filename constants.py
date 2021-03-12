SIMULATION_ITERATIONS = 10_000

# Note that "Ace" can be 1 or 11 depending on the situation! This is adjusted
# by the helpers.value_of function to give the 'best' value.
RANK_AND_VALUE = {
    "Ace": 11,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
}

SUITS = ["Hearts", "Spades", "Diamonds", "Clubs"]

NUMBER_OF_DECKS = 1

ALL_CARDS_IN_DECK = NUMBER_OF_DECKS * [[_, __] for _ in RANK_AND_VALUE for __ in SUITS]

PLAYER_CHOICES = ["HIT", "STAND"]
