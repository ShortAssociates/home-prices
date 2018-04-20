# Development Exercise:  Executive Summary

### The program

This program was written on Saturday afternoon and I stayed within the overall idea of the exercise that it should take a few hours to write.  This requirement gives me the ability to put on display some of my ideas about getting programs out quickly but also thinking longer term so it can be configured for larger projects or uses.

The overall architecture is in 2-parts:
1.	The data manipulation module (data.py)
2.	The front end (home-prices.py)
The idea here is to encapsulate all the calculations and data in the HomeData object and simply deliver pre-calculated data to the front end.  The front end using the data pulled from HomeData handles the graphing.   This is the start of a common practice to split the data from the front end, especially in web-based applications.

I selected to use Flask to present the data via a web front end.  Flask is quick and easy for projects such as this one.  The data can be presented simply with minimal html. 

The code is commented with areas of expansion and areas where I cut corners to save some time during the initial development.  This allows everyone to see where the program would be expanded for reuse as follows: 
1.	The HomeData object uses a number of hard-coded static data elements (specified by using all CAPS in my code).
2.	All the hard coded data would be listed in a configuration file.  I noted in the code that I would use the built-in configparser in Python, but the actual choice would mirror how configurations are handled in the firm:  ini, environment variables, command line options, yaml, json, hocon, etc…
3.	The html for this project is very basic and included directly in the Python code.  For larger projects or ones that would be reused, I would replace this with a template-based system such as jinja.  
4.	From a calculation standpoint, I used simple averages, if I had more time, I would have calculated weighted averages for each chart.
5.	There is NO security built into this program.
6.  I did not write full unit/integration tests.  See the code in data.py for the testing I was using during development. 
I have found working in DevOps and as an SRE, you are asked to complete a task quickly.  However, it’s important to keep some basic structures to allow simple refactoring and expansion in the future.

### Results

Using numpy, I calculated a correlation coefficient for each graph.  In addition to visually observing the correlation, the numerical calculation allows me to determine the better fit when two charts are very close in correlation.

The New York market showed the greatest correlation between price and inventory.  However, as you viewed the other charts and pick out the lowest correlation in Vermont, the correlation is not as tight as it is in New York.  I didn’t calculate any additional states, but it would be very interesting to see if Vermont was an outlier or more common when all 50 states and DC are calculated. 

My conclusion from the data, is the correlation between housing prices and inventory is strong but must feed off factors that are not necessarily included in this analysis.  New York, with the nations largest market is highly correlated, yet that may be factors not as common in other markets.  A sample of 5 states is insufficient to adjust for random chance.

# Home Prices


### Prerequisites

This has only be run on OS X and Linux.  I am unsure if this program will work in Windows.  I suspect it will not due to the different directory naming conventions.

### Installing

* Unpack the archive into a directory.
* On Linux and OS X run the Makefile
```
make install
```

an alternative to make is to run the following command to ensure all the correct modules are installed.

```
pip install -r requirements.txt
```
If you do not have sufficient rights, sudo may be required.


## Running the Program

1. Install the program onto your test system
2. Change directory to home-prices
3. execute 'run'
```
cd home-prices
./run
```
alternatively run the Python module directly:
```
cd home-prices/home-prices
python home-prices.py
```

Once running you will see the following output:
```
/usr/bin/python2.7 /home/paul/git/home-prices/home-prices/home-prices.py
2018-03-18 22:41:32,815 - DEBUG - Loading state name data
2018-03-18 22:41:32,818 - DEBUG - Loading price data file
2018-03-18 22:41:34,035 - DEBUG - Loading price data file
2018-03-18 22:41:36,341 - DEBUG - Data load complete
2018-03-18 22:41:36,342 - DEBUG - Consolidating inventory data
2018-03-18 22:41:43,190 - DEBUG - Consolidating pricing data
2018-03-18 22:41:47,274 - DEBUG - Saving data to disk
2018-03-18 22:41:47,274 - DEBUG - Data consolidation complete
2018-03-18 22:41:47,275 - DEBUG - Loading saved consolidated data
2018-03-18 22:41:47,277 - INFO -  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```
The first time you launch the program it will take 15-20 seconds to load.  During the load, it runs all the required calculations for the charts.  The calculated data is save to disk.  The next time you run the program, it will load the pre-calculated data files:
```
/usr/bin/python2.7 /home/paul/git/home-prices/home-prices/home-prices.py
2018-03-18 22:43:32,618 - DEBUG - Loading saved consolidated data
2018-03-18 22:43:32,619 - DEBUG - Loading saved consolidated data
2018-03-18 22:43:32,621 - INFO -  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

 
Open a browser and load the following address:
```
http://localhost:8080/
```
If you are on another machine, replace localhost with the name of the system running the program.  This is an example from testing:
```
http://neptune:8080/
```

The output is displayed on a single static web page.



## Built With

Python with the following external libraries installed
* Flask:  [http://flask.pocoo.org/](http://flask.pocoo.org/)
* matplotlib:  [https://matplotlib.org/](https://matplotlib.org/)
* numpy:  [http://www.numpy.org/](http://www.numpy.org/)
* pandas:  [https://pandas.pydata.org/](https://pandas.pydata.org/)

