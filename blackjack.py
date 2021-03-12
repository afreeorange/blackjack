import strategies
from constants import SIMULATION_ITERATIONS
from entities import Game


def simulate_game_with(strategy):
    """
    Simple helper to keep track of wins, losses, and draws from the Player's
    perspective.
    """

    wins, losses, pushes = 0, 0, 0

    for i in range(0, SIMULATION_ITERATIONS):
        _ = Game(strategy, silent=True)
        _.run()

        if _.winner:
            if _.winner.name == "Player":
                wins += 1
            else:
                losses += 1
        else:
            pushes += 1

    win_percentage = wins / SIMULATION_ITERATIONS * 100
    loss_percentage = losses / SIMULATION_ITERATIONS * 100
    push_percentage = pushes / SIMULATION_ITERATIONS * 100

    print(
        f"{win_percentage:.2f}% wins, "
        f"{loss_percentage:.2f}% losses, "
        f"{push_percentage:.2f}% draws "
        f"({win_percentage + loss_percentage + push_percentage:.2f}%)"
    )


# ------------

print("=" * 72)
print("Verbose single game for logging and sanity checks")
print("Player is using the 'Keep Hitting' strategy (if you can call it that.)\n")

g = Game(strategies.always_hit)
g.run()

if g.winner:
    print(f"{g.winner.name} wins")
else:
    print("Nobody wins")

# ------------

print("=" * 72)
print(f"Simulating {SIMULATION_ITERATIONS} games with each strategy")

STRATEGIES_TO_TRY = [
    strategies.always_hit,
    strategies.always_stand,
    strategies.stand_after_threshold(10),
    strategies.stand_after_threshold(11),
    strategies.stand_after_threshold(12),
    strategies.stand_after_threshold(13),
    strategies.stand_after_threshold(14),
    strategies.stand_after_threshold(15),
    strategies.stand_after_threshold(16),
    strategies.stand_after_threshold(17),
    strategies.stand_after_threshold(18),
    strategies.stand_after_threshold(19),
    strategies.stand_after_threshold(20),
    strategies.optimal_hard,
    strategies.optimal_soft,
]

for s in STRATEGIES_TO_TRY:
    print("-" * 72)
    _ = s.__doc__.split("\n")[0]
    print(f"{_}")

    simulate_game_with(s)
