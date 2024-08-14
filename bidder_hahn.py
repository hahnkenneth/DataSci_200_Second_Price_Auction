'''
This module creates a Bidder class that is based on the  Upper Confidence
Bound Method. The Bidder will keep track of how many times it's seen a specific user,
calculate how much profit they gained (if they won and the user clicked),
and calculate the user\'s UCB. 

When it comes time to bid, the bidder will remember the user_id. If the bidder has 
seen the user < 10 times, then it will bet high. If the bidder has seen the user
>= 10 times, it will either see if the user has the highest UCB, in which case the
bidder will bet high while still gaining a profit. If the user_id is not the highest,
it will bet a random number from 0 to 0.5.
'''

import math
import numpy as np

class UCBBidder:
    '''Class to represent a bidder in an online second-price ad auction'''    
    def __init__(self, num_users=1, num_rounds=1):
        '''Setting initial balance to 0, number of users, number of rounds, and round counter'''
        self.winning_prices = [0 for i in range(num_rounds)]
        self.user_profit = [0 for i in range(num_users)]
        self.user_won_auction = [0 for i in range(num_users)]
        self.user_ucb = [0 for i in range(num_users)]
        self.user_prob = [0 for i in range(num_users)]
        self.balances_over_time = [0]
        self.balance = 0
        self.current_user_id = ''
        self.round_counter = 0
    def __repr__(self):
        '''Return Bidder object with balance'''
        if self.balance < 0:
            return f'Bidder object with balance -${abs(self.balance)}'
        return f'Bidder object with balance ${self.balance}'
    def __str__(self):
        '''Return Bidder object with balance'''
        if self.balance < 0:
            return f'Bidder object with balance -${abs(self.balance)}'
        return f'Bidder object with balance ${self.balance}'
    def bid(self, user_id):
        '''Returns a non-negative bid amount. The bid amount will be based on a variation of the
        Upper Confidence Bound (UCB) Method'''
        self.current_user_id = user_id
        if self.user_won_auction[user_id]<10:
            bids = 1
        elif self.user_won_auction[user_id] >= 10:
            if self.user_ucb.index(max(self.user_ucb)) == user_id:
                bids = 0.99
            else:
                bids = round(np.random.uniform(0,self.user_prob[self.current_user_id]),3)
        return bids
    def notify(self, auction_winner, price, clicked):
        '''Updates bidder attributes based on results from an auction round'''
        self.winning_prices.append(price)
        #Will keep a track of the bidder's balance whether they won or not.
        if auction_winner:
            self.user_won_auction[self.current_user_id] += 1
            if clicked:
                self.balance += 1 - price
                self.user_profit[self.current_user_id] += 1 - price
                self.round_counter += 1
            else:
                self.balance -= price
                self.user_profit[self.current_user_id] -= price
                self.round_counter += 1
            #Find new probability of the user by dividing profit over number of times seen with user
            self.user_prob[self.current_user_id] = self.user_profit[self.current_user_id]/self.user_won_auction[self.current_user_id]
            #Use UCB1 Formula to calculate the new user's likelihood of betting more
            self.user_ucb[self.current_user_id] = self.user_prob[self.current_user_id] + math.sqrt((2*math.log(self.round_counter) / (self.user_won_auction[self.current_user_id])))
        self.balances_over_time.append(self.balance)
