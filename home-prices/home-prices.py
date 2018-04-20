##!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 This is the main program - data is being pulled from the HomeData object to make the display and graphing of
 data much easier.  The data will be served up via Flask
"""

import base64
from cStringIO import StringIO
from flask import Flask
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import signal
import sys

from data import HomeData

# Basic html for displaying the graphs - would use jinja2 templates for a larger project
html = '''
<html>
    <head>
        <title> Correlation of Home Inventory to Home Prices 2011-2016 </title>
    <body bgcolor="black" text="white">
        <center>
        <h1> Correlation of Home Inventory to Home Prices 2011-2016 </h1>
        </br>
        <img src="data:image/png;base64,{}" />
        <img src="data:image/png;base64,{}" />
        <img src="data:image/png;base64,{}" />
        <img src="data:image/png;base64,{}" />
        <img src="data:image/png;base64,{}" />
        </br>
        </br>
        <h3>
            Maximum Correlation = {} </br>
            Minimum Correlation = {} </br>
        </h3>
        </center>
    </body>
</html>
'''

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)


#  Flask entry point(s)
@app.route("/")
def display_plots():
    # Note: the hd class is in scope here since this is actually called from the app.run() in main
    data = []

    # Iterate through the states and create a graph for each state - save each into the data structure
    for state in range(0,hd.CALC_STATES):
        df = pd.DataFrame(data={'Prices': hd.get_state_price_change(state), 'Inventory': hd.get_state_inventory(state)},
                          index=hd.get_years())
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        df.plot(ax=ax, title="State: {} Corr: {:.2f}".format(hd.get_statename(state),hd.get_correlation(state)), secondary_y='Inventory', figsize=(4,4))
        io = StringIO()
        fig.savefig(io, format='png')
        data.append(base64.encodestring(io.getvalue()))

    # for ease of development, I hard coded the number of graphs
    return html.format(data[0], data[1], data[2], data[3], data[4], hd.get_max_correlation(), hd.get_min_correlation())


# Capture the keyboard interrupt to gracefully shutdown
def signal_handler(signal, frame):
    logging.debug("Keyboard interrupt - exiting __file__")
    sys.exit(0)


if __name__ == '__main__':
    hd = HomeData()
    hd.load_data()
    signal.signal(signal.SIGINT, signal_handler)  # setup the keyboard interrupt before launching the webserver
    app.run(host='0.0.0.0', port=8080)
