##!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Module to abstract the data for use in the main program.  The data will be imported here
 then presented to the other modules.  There are a few functions that were added but not used
"""

import logging
import numpy
import os.path
import pickle


class HomeData:
    # Using hard coded defaults to for this exercise to save time
    # these would be configurable using the Python configparser module if used in a production app
    NUM_PRICE_COLS = 72
    NUM_INVENTORY_COLS = 72
    NUM_YEARS = 6
    CALC_STATES = 5
    YEARS = ['2011', '2012', '2013', '2014', '2015', '2016']
    STATES = ['New Jersey', 'California', 'Vermont', 'Colorado', 'New York']
    STATESA = ['NJ', 'CA', 'VT', 'CO','NY']

    def __init__(self, data_dir='../data/'):
        self.data_dir = data_dir
        self.inventory = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])
        self.prices = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])
        self.correlation=[]
        self.load_data()
        self.calculate_correlation()
        return

    # Here are a number of methods to pull data from the class so the underlying data does not need to be exposed
    def get_states(self):
        return self.STATES

    def get_statename(self, state):
        return self.STATES[state]

    def get_years(self):
        return self.YEARS

    def get_state_inventory(self, state):
        return self.inventory[state]

    def get_state_price_change(self, state):
        return self.prices[state]

    def refresh_data(self):
        self.load_data(reload=True)

    def get_min_correlation(self):
        return self.STATES[numpy.argmin(self.correlation)]

    def get_max_correlation(self):
        return self.STATES[numpy.argmax(self.correlation)]

    def get_correlation(self, state):
        return self.correlation[state]

    def calculate_correlation(self):
        for state in range(0, self.CALC_STATES):
            R = numpy.corrcoef(self.inventory[state], self.prices[state])
            self.correlation.append(R[0][1])
        return True

    def load_data(self, reload=False):
        # Read state names into dictionary - create lookups for both state and abbreviation
        # To save time during development, I saved the data using pickle to save about 5 seconds during startup.
        if os.path.isfile("{}{}".format(self.data_dir,"inventory.p")) \
                and os.path.isfile("{}{}".format(self.data_dir,"prices.p")) \
                and (reload==False):
            logging.debug("Loading saved consolidated data")
            self.inventory = pickle.load(open("{}{}".format(self.data_dir,"inventory.p"), "rb"))
            self.prices = pickle.load(open("{}{}".format(self.data_dir,"prices.p"), "rb"))
            return True

        logging.debug("Loading state name data")
        self.statenames = dict(numpy.genfromtxt('{}{}'.format(self.data_dir, 'states.csv'), delimiter=',',
                                           dtype=None, names=True))

        logging.debug("Loading price data file")
        # The configuration to load the data can be moved into a config file to make it easier to modify
        # for additional data types
        all_prices = numpy.genfromtxt('{}{}'.format(self.data_dir, 'MedianPriceReductionPct.csv'), delimiter=',',
                                      dtype=None, names=True,
                                      usecols=(4,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,
                                                 34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,
                                                 57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
                                                 80,81,82
                                                 )
                                      )

        logging.debug("Loading price data file")
        all_inventory = numpy.genfromtxt('{}{}'.format(self.data_dir, 'HomeInventory.csv'), delimiter=',',
                                          dtype=None, names=True,
                                          usecols=(5,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,
                                                   41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,
                                                   64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,
                                                   87,88,89,90
                                                  )
                                          )

        logging.debug("Data load complete")
        self.consolidate_data(all_inventory, all_prices)
        return True

    # This will read through the datasets and create the consolidated data for analysis - the output is 2 matrix's
    # of pricing data and inventory data by state
    def consolidate_data(self, all_inventory, all_prices):

        sum = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])
        count = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])

        # consolidate the inventory data
        # this is BRUTE FORCE... has not been optimized
        logging.debug("Consolidating inventory data")
        for row in all_inventory:
            for x in range(0,self.CALC_STATES ):
                if self.STATES[x] in row:
                    for a in range(0,self.NUM_INVENTORY_COLS):
                        b,c = divmod(a,12)
                        sum[x][b] += row[a+1]
                        count[x][b] +=1
        self.inventory = sum/count

        # Zero out the count matrix
        count = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])
        sum = numpy.zeros([self.CALC_STATES, self.NUM_YEARS])

        # Sum price data into temporary structures, again brute force then divide the two matrix's
        logging.debug("Consolidating pricing data")
        for row in all_prices:
            for x in range(0, self.CALC_STATES):
                if self.STATESA[x] in row:
                    for a in range(0,self.NUM_PRICE_COLS):
                        b,c = divmod(a,12)
                        sum[x][b] += row[a+1]
                        count[x][b] += 1
        self.prices = sum/count

        # Save data locally for faster retrieval
        logging.debug("Saving data to disk")
        pickle.dump(self.inventory,open("{}{}".format(self.data_dir,"inventory.p"), "wb"))
        pickle.dump(self.prices,open("{}{}".format(self.data_dir,"prices.p"), "wb"))
        logging.debug("Data consolidation complete")
        return True

    def print_data(self):
        # This is here for testing purposes
        print self.inventory
        print self.prices


if __name__ == '__main__':

    # I didn't create unit tests during development, however, I was testing the module by running this directly.
    # I left all this code here to see how I was testing during development.  Once released this would be replaced with
    # a simple method stating "this file is not intended to run directly"
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    print "Testing HomeData Class"
    hd = HomeData()
    print hd.get_state_price_change(0)
    print hd.get_state_inventory(0)
    print hd.get_states()
    print hd.get_years()
    for state in range(0, hd.CALC_STATES):
        print hd.get_correlation(state)
    print "Maximum Correlation = ", hd.get_max_correlation()
    print "Minimum Correlation = ", hd.get_min_correlation()

    hd.refresh_data()
    print hd.get_state_price_change(0)
    print hd.get_state_inventory(0)
    print hd.get_states()
    print hd.get_years()
    for state in range(0, hd.CALC_STATES):
        print hd.get_correlation(state)
    print "Maximum Correlation = ", hd.get_max_correlation()
    print "Minimum Correlation = ", hd.get_min_correlation()

    hd.print_data()

