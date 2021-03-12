import random

from constants import RANK_AND_VALUE


def pick_a_card(deck_or_deck_of_decks, tracker):
    card = None
    available_cards = [
        _ for _ in filter(lambda _: _ not in tracker, deck_or_deck_of_decks)
    ]

    if len(available_cards) == 0:
        raise Exception("No more cards left to deal!")

    while True:
        card = random.choice(deck_or_deck_of_decks)

        if card not in tracker:
            tracker.append(card)
            break

    return card


def value_of(hand):
    """
    Determine the value of a card or cards, adjusting for the Ace. No splitting
    of Aces or anything of the sort. Just give the 'best' value of a hand.

    E.g.

    (9, 10, Ace) = 20
    (A, A, 10) = 12
    (A, A, A) = 13
    (A, A) = 12
    (K, Q, A) = 21
    (7, 4, A) = 12
    """
    value = sum(RANK_AND_VALUE[card[0]] for card in hand)
    number_of_aces = len([card for card in hand if card[0] == "Ace"])

    if number_of_aces == 0:
        return value

    for _ in range(0, number_of_aces):
        if value > 21:
            value = value - 10
        else:
            break

    return value
