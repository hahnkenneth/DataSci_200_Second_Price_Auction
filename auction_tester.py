#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:23:18 2024

@author: kennethhahn
"""

# %% initialize modules and classes

import auction_hahn as a
from bidder_hahn import Bidder as UCB
import numpy as np
import matplotlib.pyplot as plt
import math

class RandomBidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    
    def __init__(self, num_users=0, num_rounds=0):
        '''Setting initial balance to 0, number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.clicked = None
        self.winning_price = 0
        self.balance = 0
        self.balances_over_time = [0]
        self.bids_over_time = [0]

    def __repr__(self):
       '''Return Bidder object with balance'''
       if self.balance < 0:
           return f'This bidder has a balance of -${abs(self.balance)}'
       else:
           return f'This bidder has a balance of ${self.balance}'

    def __str__(self):
        '''Return Bidder object with balance'''
        if self.balance < 0:
            return f'This bidder has a balance of -${abs(self.balance)}'
        else:
            return f'This bidder has a balance of ${self.balance}'

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        #return 200
        bids = round(np.random.uniform(0,1),3)
        self.bids_over_time.append(bids)
        return bids
        #return 100

    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        if auction_winner:
            self.balance -= round(price,3)
            if clicked:
                self.balance += 1
            self.balances_over_time.append(self.balance)
            
        else:
            self.winning_price = price
            self.balances_over_time.append(self.balance)

class EpsilonGreedyBidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    
    def __init__(self, num_users=0, num_rounds=0, epsilon=0.1):
        '''Setting initial balance to 0, number of users, number of rounds, and round counter'''
        self.num_rounds = num_rounds
        self.num_users = num_users
        self.round_counter = 0
        self.winning_prices = [0 for i in range(num_rounds)]
        self.user_clicked = [0 for i in range(num_users)]
        self.user_won_auction = [0 for i in range(num_users)]
        self.user_ucb = [0 for i in range(num_users)]
        self.user_prob = [0 for i in range(num_users)]
        self.balance = 0
        self.epsilon = epsilon
        self.balances_over_time = [0]
        self.bids_over_time = [0]

    def __repr__(self):
       '''Return Bidder object with balance'''
       if self.balance < 0:
           return f'This bidder has a balance of -${abs(self.balance)}'
       else:
           return f'This bidder has a balance of ${self.balance}'

    def __str__(self):
        '''Return Bidder object with balance'''
        if self.balance < 0:
            return f'This bidder has a balance of -${abs(self.balance)}'
        else:
            return f'This bidder has a balance of ${self.balance}'

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        #return 200
        self.current_user_id = user_id
        if np.random.uniform() < self.epsilon:
            bids = round(np.random.uniform(),3)
        else:
            if self.user_prob[self.current_user_id] == max(self.user_prob):
                bids = 0.99
            else:
                bids = round(np.random.uniform(0,0.99),3)
                
        self.bids_over_time.append(bids)
        return bids
        #return 100

    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        if auction_winner:
            self.user_won_auction[self.current_user_id] += 1
            
            if clicked:
                self.balance += 1 - price
                self.user_clicked[self.current_user_id] += 1 - price
            else:
                self.balance -= price
                self.user_clicked[self.current_user_id] -= price
                
            self.user_prob[self.current_user_id] = self.user_clicked[self.current_user_id]/self.user_won_auction[self.current_user_id]
        
        self.balances_over_time.append(self.balance)

# %% Initialize Variables
users = []
bidders = []
game = np.nan
num_rounds = 10000
num_users = 100
users =  [a.User() for i in range(num_users)]
epsilon_bidders = [EpsilonGreedyBidder(num_users,num_rounds,i) for i in np.arange(0.1,1,0.1)]
bidders = [RandomBidder(),UCB(num_users,num_rounds)]
all_bidders = bidders + epsilon_bidders

game = a.Auction(users,all_bidders)

for i in range(num_rounds):
    game.execute_round()

plt.figure()
for i,bidder in enumerate(all_bidders):
    plt.plot(bidder.balances_over_time)
    print(f'Length of balances over time = {len(bidder.balances_over_time)}')

label1=['Random','UCB']
label2 = [f'EpsilonGreedy-0{i+1}' for i in range(len(epsilon_bidders))]

label = label1 + label2

plt.legend(labels=label,loc='center left',bbox_to_anchor = (1,0.5))
plt.title(f'Balances Over Time with n = {num_users} Users')
plt.xlabel('Number of Rounds')
plt.ylabel('Balances')
plt.show()
# %% plot final balances
