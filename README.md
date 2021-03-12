# MiniProject I - BlackJack Simulation

👉 Please note: This README is meant to be both a small report (the first half) and developer notes (second half.)

## Running

Requires Python 3.8+ and nothing else (it's all Standard Library stuff.)

```bash
# Simulate 10,000 games for each strategy with a single deck
python blackjack.py
```

See the "Development" section for other programmatic details.

## Introduction

Simulates many Blackjack games with assorted strategies and all the usual rules[1] _except_ that a player _cannot_ double-down or split. They can only hit or stand. The goal is to find the best strategy that maximizes the player's chances of winning. This is expressed as a win-percentage at the end of each round of simulation with a specific strategy. Draws/pushes do not count as winning.

### A Note on Randomness

No custom random number generators were used. From the Python documentation[2], the base `random` function generates `~Unif(0,1)` PRNGs with a cycle length of (2<sup>19,937</sup> - 1). Because this is a simulation and not programmatic unit testing, I didn't see the need to create my own generator.

## Strategies

This simulation employs three classes of strategies, two of which are 'blind' to the dealer's face card.

### Always Hit or Always Stand (Blind)

These are the most naïve strategies. In both, the player goes YOLO and hopes for BlackJack.

If they don't get one with their first draw, they either stand (this is what I'd do if I were drunk), or they just keep hitting until it's BlackJack-or-Bust (this is what I'd do if I were _reaaaally_ drunk.)

### Stand After Threshold (Blind)

Hit until you meet or exceed a given threshold for your cards' value and stand once this is reached. I put these in since this is how I myself would play BlackJack as an amateur (i.e., no card-counting or memorizing strategies. Or alcohol.) I think most amateurs would do this. E.g. "Oh it looks like I'm at 18. Maybe I should drink this awful Vodka-flavoured 'drink' and stop getting more cards."

The only downside here is that this does _not_ take into account the Dealer's hand. Just what's in front of me. Having never known of the rules of BlackJack before this project, I couldn't find a way to incorporate this information into my strategy; this is definitely an area for improvement.

### Use established 'Optimal Strategies'

There are two 'optimal' strategies in `strategies.py` which are based on the references in the `misc/` folder. Both images are different presentations of the same mathematically determined strategies that take into account both your and the dealer's hand.

Please note that since we don't have double-downs in our simulation, the "D"s are "H"s: If the strategy cards say we should double-down, we hit #YOLO

## Results

These were rather shocking to me. Having never played BlackJack (yep), I thought they were totally wrong because the winning percentages were so high. However, I found out that the probability of a _net win_ in BlackJack is 42.43%[3]. This is reassuring, assuming it is right (it still seems unbelievably high.)

With that in mind, here are the results of **one million runs** of all strategies:

```
========================================================================
Simulating 1000000 games with each strategy
------------------------------------------------------------------------
Strategy: Always be hitting
18.32% wins, 81.67% losses, 0.00% draws (100.00%)
------------------------------------------------------------------------
Strategy: Always be standing
38.59% wins, 57.16% losses, 4.25% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 10
39.39% wins, 55.44% losses, 5.17% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 11
40.54% wins, 53.70% losses, 5.76% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 12
42.35% wins, 51.87% losses, 5.79% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 13
42.88% wins, 50.46% losses, 6.66% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 14
43.16% wins, 49.49% losses, 7.35% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 15
42.70% wins, 49.38% losses, 7.92% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 16
43.34% wins, 48.58% losses, 8.08% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 17
42.88% wins, 48.60% losses, 8.53% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 18
41.20% wins, 51.55% losses, 7.25% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 19
38.15% wins, 56.43% losses, 5.42% draws (100.00%)
------------------------------------------------------------------------
Strategy: Stand After Threshold 20
31.23% wins, 65.00% losses, 3.77% draws (100.00%)
------------------------------------------------------------------------
Strategy: Optimal Hard
43.88% wins, 48.32% losses, 7.80% draws (100.00%)
------------------------------------------------------------------------
Strategy: Optimal Soft
44.25% wins, 47.62% losses, 8.13% draws (100.00%)
```

### Always Hit or Always Stand (Blind)

It would appear that the **worst** strategy is the most aggressive one: always keep hitting. This makes intuitive sense. 

Going the other way and being defensive/conservative by standing immediately yields ~2x better results.

### Stand After Threshold (Blind)

I tried this with all possible values from 10-20. 

Of all the thresholding strategies, it would appear that standing "somewhere in the middle" between 13 and 17 gives the best results. I'll pick the median 15 to be the best value to stand on if you don't know what you're doing and are basing your moves only on what's in front of you.

### Use established 'Optimal Strategies'

These yielded the **best results** with almost all runs of my simulation and are rather marvelous. I was unable to find a resource over how the strategies were determined (maybe through simulation!)

## References

1. [Bicycle Cards: How to play BlackJack](https://bicyclecards.com/how-to-play/blackjack/)
2. [Python: Generate pseudo-random numbers](https://docs.python.org/3/library/random.html)
3. [Variance in BlackJack](https://wizardofodds.com/games/blackjack/variance/) (see the "_Probability of Net Win_" section.)

--- 

## Development

All modules [contain what you think they contain](https://en.wikipedia.org/wiki/Principle_of_least_astonishment).

### Strategies

These are in a module called `strategies.py`. Please see the docstrings for each function for what they do. 

**You can add your own strategies**! Just add them to `strategies.py`, remembering to have the following method signature

```
my_strategy(player_hand, dealer_face_up_card) -> "HIT" | "STAND"
```

Here, `player_hand` will be given to you as a simple array that looks like this:

```
[
    ['Five', 'Hearts'],
    ['Eight', 'Hearts'],
    ['Five', 'Spades'],
    ['Nine', 'Spades'],
]
```

Whereas the `dealer_face_up_card` would simply be something like `['King', 'Hearts']`. Make sure that your function only returns a `HIT` or `STAND`. Then add your strategy function to `STRATEGIES_TO_TRY` in `blackjack.py` and run the simulation 🚀

### Adjustments

* You can change the number of iterations in the simulation by opening `constants.py` and adjusting `SIMULATION_ITERATIONS`.
* In the same module, you can change the number of decks in the same file by tweaking `NUMBER_OF_DECKS`. This simulation uses just one deck by default.
