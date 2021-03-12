import random

from helpers import pick_a_card, value_of
from constants import ALL_CARDS_IN_DECK


class Agent:
    """
    This can be either a Player or a Dealer. Maintains track of their hand and
    the value of their hand. Instantiate with `is_dealer` set to `True` if you
    want to create a Dealer.
    """

    def __init__(self, is_dealer=False):
        self.name = "Dealer" if is_dealer else "Player"
        self.is_dealer = is_dealer
        self.hand = []

    def deal_card(self, card):
        self.hand.append(card)

    @property
    def value(self):
        return value_of(self.hand)


class Game:
    """
    The Game 'engine'. Create using a given `player_strategy` (see README),
    specify whether or not you'd like verbose logging of the game, and supply
    it a deck of cards.

    Once you have a game instance, and just like in real-life, run

    Game.simulate_player()
    Game.simulate_dealer()
    Game.finish_game()

    explicitly, or just go Game.run()
    """

    def __init__(self, player_strategy, silent=False, deck=ALL_CARDS_IN_DECK):
        self.dealer = Agent(True)
        self.player = Agent()

        self.deck = deck
        random.shuffle(self.deck)
        self.card_tracker = []

        self.player_strategy = player_strategy
        self.silent = silent
        self.winner = None

        self.__print("Dealing cards...")

        self.dealer.deal_card(self.__get_card())
        self.player.deal_card(self.__get_card())
        self.dealer.deal_card(self.__get_card())
        self.player.deal_card(self.__get_card())

        self.__print_cards(self.dealer)
        self.__print_cards(self.player)

    def __print(self, message):
        if not self.silent:
            print(message)

    def __print_cards(self, agent):
        if not self.silent:
            if agent.name == "Dealer":
                print(f"{agent.name} shows {agent.hand[0][0]} of {agent.hand[0][1]}")
            else:
                print(f"{agent.name} has {agent.hand} ({agent.value})")

    def __get_card(self):
        return pick_a_card(self.deck, self.card_tracker)

    def simulate_player(self):
        """
        As a player,

        1. If the value of your cards is 21, congrats! You win!
        2. If it's over 21, tough luck. You lose.
        3. Depending on the strategy employed, either hit or stay

        Loop.
        """

        if self.player.value == 21:
            self.__print("Player has Blackjack!")
            self.declare_winner(self.player)
            return

        if self.player.value > 21:
            self.__print(f"Player has busted ({self.player.value})")
            self.declare_winner(self.dealer)
            return

        # Figure out what to do (HIT or STAND)
        action = self.player_strategy(self.player.hand, self.dealer.hand[0])

        if action == "HIT":
            self.__print("Player chose to hit!")
            self.player.deal_card(self.__get_card())
            self.__print_cards(self.player)

            self.simulate_player()
        elif action == "STAND":
            self.__print("Player stays")
        else:
            raise ValueError(
                f"Action must be either 'HIT' or 'STAND'. Received '{action}'"
            )

    def simulate_dealer(self):
        """
        Keep pulling cards until you

        1. Get more than the player, in which case you win
        2. Are at 17 or more, at which point you stay there
        """

        # Nothing to do if we already have a winner...
        if self.winner:
            return

        self.__print(
            f"Dealer flips other card: "
            f"it's {self.dealer.hand[1][0]} of {self.dealer.hand[1][1]} "
            f"({self.dealer.value})"
        )

        while True:
            if self.dealer.value < 17:
                self.dealer.deal_card(self.__get_card())
                self.__print(
                    f"Dealer pulls a {self.dealer.hand[-1][0]} "
                    f"of {self.dealer.hand[-1][1]} "
                    f"({self.dealer.value})"
                )
            else:
                break

    def finish_game(self):
        """
        1. If the dealer has over 21, dealer loses
        2. If the dealer has a Blackjack, dealer wins
        3. If the dealer's value exceeds the player's, dealer wins
        4. If the dealer's value equals the players, nobody wins
        5. If the dealer's value is less than the player's, player wins
        """

        # Nothing to do if we already have a winner...
        if self.winner:
            return

        if self.dealer.value > 21:
            self.declare_winner(self.player)

        elif self.dealer.value == 21:
            self.declare_winner(self.dealer)

        elif self.dealer.value > self.player.value:
            self.declare_winner(self.dealer)

        elif self.dealer.value == self.player.value:
            self.declare_winner(None)

        elif self.dealer.value < self.player.value:
            self.declare_winner(self.player)

    def declare_winner(self, winner):
        self.winner = winner

    def run(self):
        self.simulate_player()
        self.simulate_dealer()
        self.finish_game()
