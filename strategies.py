"""
Player strategy expressed as functions. Because functions are first-class in
Python, we can pass them to a `Game` instance to simulate what a player would
do.

The contract here is that each function, regardless of how complicated its
decision algorithm might get, takes in the player's hand (which is a list of
two or more cards) and the dealer's card (only one... that's all that's shown!)
and returns either a "HIT" or "STAND". Just like in real life :) It might be
that neither of these inputs is used in coming up with a decision.
"""

from helpers import value_of


def always_hit(players_hand, dealer_card_shown):
    """Strategy: Always be hitting

    About as simple and stupid as it gets. Keep hitting until you get 21 or
    bust. Life's too short. Live on the edge. YOLO.
    """
    if value_of(players_hand) < 21:
        return "HIT"
    else:
        return "STAND"


def always_stand(players_hand, dealer_card_shown):
    """Strategy: Always be standing

    Just be happy with the two cards you're dealt. #Gratitude 🙏
    """
    return "STAND"


def stand_after_threshold(threshold):
    """
    Hit until you are at or above the supplied threshold value and then stand
    after that.
    """

    def inner(players_hand, dealer_card_shown):
        if value_of(players_hand) < threshold:
            return "HIT"
        else:
            return "STAND"

    inner.__doc__ = f"""Strategy: Stand After Threshold {threshold}

    Hit only if the value of your cards is under a certain threshold.
    """

    return inner


def optimal_hard(players_hand, dealer_card_shown):
    """Strategy: Optimal Hard

    See misc/optimal-strategy.png for a reference. Since there's no
    doubling-down in this simulation, doubles are hits.
    """

    # To be read as: "When the value of my hand is (key) and the dealer's
    # face-up card is (key -> value), do (value)"
    strategy = {
        20: {
            "Ace": "STAND",
            "Two": "STAND",
            "Three": "STAND",
            "Four": "STAND",
            "Five": "STAND",
            "Six": "STAND",
            "Seven": "STAND",
            "Eight": "STAND",
            "Nine": "STAND",
            "Ten": "STAND",
            "Jack": "STAND",
            "Queen": "STAND",
            "King": "STAND",
        }
    }
    strategy[19] = strategy[20]
    strategy[18] = strategy[20]
    strategy[17] = strategy[20]

    strategy[16] = {
        "Two": "STAND",
        "Three": "STAND",
        "Four": "STAND",
        "Five": "STAND",
        "Six": "STAND",
        "Seven": "HIT",
        "Eight": "HIT",
        "Nine": "HIT",
        "Ten": "HIT",
        "Jack": "HIT",
        "Queen": "HIT",
        "King": "HIT",
        "Ace": "HIT",
    }
    strategy[15] = strategy[16]
    strategy[14] = strategy[16]
    strategy[13] = strategy[16]

    strategy[12] = {
        "Two": "HIT",
        "Three": "HIT",
        "Four": "STAND",
        "Five": "STAND",
        "Six": "STAND",
        "Seven": "HIT",
        "Eight": "HIT",
        "Nine": "HIT",
        "Ten": "HIT",
        "Jack": "HIT",
        "Queen": "HIT",
        "King": "HIT",
        "Ace": "HIT",
    }

    strategy[11] = {
        "Ace": "HIT",
        "Two": "HIT",
        "Three": "HIT",
        "Four": "HIT",
        "Five": "HIT",
        "Six": "HIT",
        "Seven": "HIT",
        "Eight": "HIT",
        "Nine": "HIT",
        "Ten": "HIT",
        "Jack": "HIT",
        "Queen": "HIT",
        "King": "HIT",
    }
    strategy[10] = strategy[11]
    strategy[9] = strategy[11]
    strategy[8] = strategy[11]
    strategy[7] = strategy[11]
    strategy[6] = strategy[11]
    strategy[5] = strategy[11]
    strategy[4] = strategy[11]
    strategy[3] = strategy[11]

    # Finally our strategy!
    return strategy[value_of(players_hand)][dealer_card_shown[0]]


def optimal_soft(players_hand, dealer_card_shown):
    """Strategy: Optimal Soft

    See misc/optimal-strategy.png for a reference. This strategy is employed
    when you have an Ace and some other card. Since there's no doubling-down
    in this simulation, doubles are hits.

    Note: This is when the other card is an Ace. If it isn't, just switch to
    the "optimal hard" strategy. This might be OK since they're part of a
    giant overall strategy anyway.
    """

    # To be read as "When you see an Ace-9 Pair (key) and dealer has (value)"
    strategy = {
        "Nine": {
            "Two": "STAND",
            "Three": "STAND",
            "Four": "STAND",
            "Five": "STAND",
            "Six": "STAND",
            "Seven": "STAND",
            "Eight": "STAND",
            "Nine": "STAND",
            "Ten": "STAND",
            "Jack": "STAND",
            "Queen": "STAND",
            "King": "STAND",
            "Ace": "STAND",
        }
    }

    strategy["Eight"] = strategy["Nine"]
    strategy["Eight"]["Six"] = "HIT"

    strategy["Seven"] = {
        "Two": "HIT",
        "Three": "HIT",
        "Four": "HIT",
        "Five": "HIT",
        "Six": "HIT",
        "Seven": "STAND",
        "Eight": "STAND",
        "Nine": "HIT",
        "Ten": "HIT",
        "Jack": "HIT",
        "Queen": "HIT",
        "King": "HIT",
        "Ace": "HIT",
    }

    strategy["Six"] = strategy["Seven"]
    strategy["Six"]["Seven"] = "HIT"
    strategy["Six"]["Eight"] = "HIT"

    strategy["Five"] = strategy["Six"]
    strategy["Four"] = strategy["Six"]
    strategy["Three"] = strategy["Six"]
    strategy["Two"] = strategy["Six"]

    # Kings, Queens, Jacks
    strategy["Ten"] = strategy["Nine"]
    strategy["Jack"] = strategy["Nine"]
    strategy["Queen"] = strategy["Nine"]
    strategy["King"] = strategy["Nine"]

    # Finally our strategy!
    #
    # If we have
    # 1) More than two cards
    # 2) No ace in our hand
    # 3) Two aces in our hand
    #
    # send to optimal hard.

    ranks = [card[0] for card in players_hand]

    if len(players_hand) > 2 or "Ace" not in ranks or ranks == ["Ace", "Ace"]:
        return optimal_hard(players_hand, dealer_card_shown)

    other_card = [card for card in players_hand if card[0] != "Ace"][0]

    return strategy[other_card[0]][dealer_card_shown[0]]
