"""
This module creates a User and an Auction Class. The User class will have a random
probability of clicking on an ad if it is chosen.

The Auction class will choose a randome user and will then have all the Bidders
bid based on the user chosen. Based on the bids, the Auction will choose the
highest bid as the winner and the second highest winner as the price that the
winner must pay. The Auction will show the ad to the user and the user will choose
to click or not. The Auction will then notify all bidders of the outcome.
"""

import numpy as np

class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''
    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.__probability =  np.random.uniform()
    def __repr__(self):
        '''User object with secret probability'''
        return f'This user has a probability {self.__probability} of clicking on an ad'
    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return f'This user has a probability {self.__probability} of clicking on an ad'
    def show_ad(self):
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        return np.random.choice([True,False],p=[self.__probability , 1 - self.__probability])
class Auction:
    '''Class to represent an online second-price ad auction'''
    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary to store balances 
        for each bidder in the auction'''
        self.users = users
        self.bidders = bidders.copy()
        self.balances = {bidder: 0 for bidder in self.bidders}
    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return 'auction'
    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return 'auction'
    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''
        user_id = np.random.randint(0,len(self.users))
        winning_indices = []
        for index,bidder in enumerate(self.bidders):
            if self.balances[bidder] < -1000:
                del self.balances[bidder]
                del self.bidders[index]
        if len(self.balances) == 0:
            return 'All Bidders are disqualified'
        bids = [bidder.bid(user_id) for index,bidder in enumerate(self.bidders)]
        max_price = max(bids)
        for index,bid in enumerate(bids):
            if bid == max_price:
                winning_indices.append(index)
        if len(winning_indices) > 1:
            winning_index = np.random.choice(winning_indices)
        else:
            winning_index = winning_indices[0]
        if len(bids) > 1:
            remaining_values = bids[:winning_index] + bids[winning_index+1:]
            winning_price = max(remaining_values)
        else:
            winning_price = max(bids)
        clicked = self.users[user_id].show_ad()
        for index,bidder in enumerate(self.bidders):
            if index == winning_index:
                bidder.notify(True,winning_price,clicked)
                self.balances[bidder] = self.balances[bidder] \
                                        + int(clicked) - winning_price
            else:
                bidder.notify(False,winning_price,None)
