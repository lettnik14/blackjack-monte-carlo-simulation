#!/usr/bin/env python
# coding: utf-8

# In[7]:


# Blackjack Monte Carlo Simulation with Dynamic Shoe Modeling 

# This project exploers blackjack strategy using Monte Carlo simulation. 
# The model evolves from independent hands to a realistic multi-deck shoe 
# with card depletion, penetration, and reshuffling. 

# The goal is to analyze expected value, variance, and risk adjusted returns 
# under different player straegies.


# In[8]:


# Core Concepts
# In this simulation I choose to use a persitent shoe - ie cards are drawn without replacement from one shoe until the shoe 
# reaches 25%. Drawing w/o replacement is necessary to simulate a proper universe. Drawing w/o replacment demonstrates odds 
# as our universe of outcomes becomes ever more narrow as the simulation goes on.


# In[9]:


import random 
from collections import Counter 
import statistics


# In[10]:


class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.build_shoe()

    def build_shoe(self):
        ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.cards = ranks * 4 * self.num_decks
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def cards_remaining(self):
        return len(self.cards)

def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)




class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        aces = 0

        for card in self.cards:
            value = card_value(card)
            total += value
        if card == 'A':
            aces += 1


        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total







def bust_probability(shoe, current_hand):
    remaining_cards = shoe.cards
    total_remaining = len(remaining_cards)

    busts = 0

    for card in remaining_cards:
        temp_hand = Hand()
        temp_hand.cards = current_hand.cards.copy()
        temp_hand.add_card(card)

        if temp_hand.value() > 21:
            busts += 1

    return busts / total_remaining




def play_round():
    shoe = Shoe()
    player = Hand()
    dealer = Hand()

    # Initial deal
    player.add_card(shoe.draw())
    player.add_card(shoe.draw())
    dealer.add_card(shoe.draw())
    dealer.add_card(shoe.draw())

    print("\n-- PLAYER TURN --")

    while True:
        total = player.value()
        print(f"Player hand: {player.cards} | Total: {total}")

        if total <= 21:
            prob = bust_probability(shoe, player)
            print(f"Probability of bust if hit: {prob:.2%}")

        if total > 21:
            print("Player busts! Dealer wins.")
            return

        action = input("Hit or Stand? ").lower()

        if action == "hit":
            player.add_card(shoe.draw())
        else:
            break

    print("\n--- DEALER TURN ---")

    while dealer.value() < 17:
        dealer.add_card(shoe.draw())

    dealer_total = dealer.value()
    player_total = player.value()

    print(f"Dealer hand: {dealer.cards} | Total: {dealer_total}")

    if dealer_total > 21:
        print("Dealer busts! Player wins.")
    elif dealer_total > player_total:
        print("Dealer wins.")
    elif dealer_total < player_total:
        print("Player wins.")
    else:
        print("Push (tie).")




def simulate(num_rounds=10000, hit_threshold=17, num_decks=6, penetration=0.75):

    shoe = Shoe(num_decks)

    reshuffle_point = int(52 * num_decks * (1-penetration))

    player_wins = 0 
    dealer_wins = 0 
    pushes = 0 
    player_busts = 0 
    dealer_busts = 0 

    results = []

    for _ in range(num_rounds):

        if shoe.cards_remaining() <= reshuffle_point:
            shoe.build_shoe()

        # NEW HANDS EACH ROUND
        player = Hand()
        dealer = Hand()

        # Initial deal 
        player.add_card(shoe.draw())
        player.add_card(shoe.draw())
        dealer.add_card(shoe.draw())
        dealer.add_card(shoe.draw())

        # Player auto-play strategy
        while player.value() < hit_threshold:
            player.add_card(shoe.draw())

        if player.value() > 21:
            player_busts += 1
            dealer_wins += 1
            results.append(-1)
            continue

        # Dealer plays
        while dealer.value() < 17:
            dealer.add_card(shoe.draw())

        if dealer.value() > 21:
            dealer_busts += 1
            player_wins += 1
            results.append(1)
        elif dealer.value() > player.value():
            dealer_wins += 1
            results.append(-1)
        elif dealer.value() < player.value():
            player_wins += 1
            results.append(1)
        else:
            pushes += 1
            results.append(0)



    # Ouput statistics 
    print("\n--- Simulation Results ---")
    print(f"Total Hands: {num_rounds}")
    print(f"Player Win Rate: {player_wins / num_rounds:.2%}")
    print(f"Dealer Win Rate: {dealer_wins / num_rounds:.2%}")
    print(f"Push Rate: {pushes / num_rounds:.2%}")
    print(f"Player Bust Rate: {player_busts / num_rounds:.2%}")
    print(f"Dealer Bust Rate: {dealer_busts / num_rounds:.2%}")

    ev = statistics.mean(results)
    std_dev = statistics.stdev(results)
    sharpe = ev / std_dev if std_dev != 0 else 0

    print(f"Expected Value per Hand: {ev:.4f}")
    print(f"Standard Deviation of Returns: {std_dev:.4f}")
    print(f"Risk-Adjusted Return (EV / StdDev): {sharpe:.4f}")





# In[ ]:





# In[ ]:





# In[ ]:





# In[11]:


## Interaction Blackjack (Manuel Play)


# In[17]:


if __name__ == "__main__":
    play_round()
    simulate(10000, hit_threshold=15)
    simulate(10000, hit_threshold=16)
    simulate(10000, hit_threshold=17)
    simulate(10000, hit_threshold=18)


# In[ ]:





# In[13]:


## Observations

# Lower hit thresholds reduce bust rate but lower upside
# Persistent shoe introduces path dependency 
# Variance increases under aggressive straedies 
# EV stabilizes as number of rounds increses 


# In[ ]:





# In[ ]:




