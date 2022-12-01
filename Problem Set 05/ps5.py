# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: VITOR CRUZ
# Collaborators (discussion):
# Time: 6h

import math
import pylab
import re
import numpy as np
from numpy.polynomial import Polynomial

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - np.mean(x))**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    
    ## LIST OF PARAMS TO PASS THROUGH THE POLYFIT FUNCTION        
    list_params = list(map(lambda degree: [x, y, degree], degs))  

    ## USE MAP TO RUN THE FUNTION TO EACH LIST OF PARAMS, RETURNING A LIST OF RESULTS    
    return list(map(lambda x: np.polyfit(*x), list_params))


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    
    mean = np.mean(y)
    numerator = ((y - estimated) ** 2).sum()
    denominator = ((y - mean) ** 2).sum()
    return 1 - float(numerator) / denominator     
    

def evaluate_models_on_training(x, y, models, title='Degrees Celsius Over the Years'):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """   
    
    ## PLOTTING ALL THE MODELS TO THE SAME GRAPH AS I DON'T HAVE TO DELIVER THE PSET. DOING IT TO SEE THE RESULTS, BUT I DON'T NEED TO FOLLOW ALL THE REQUIREMENTS.
    pylab.figure()
    pylab.plot(x, y, 'o', label = 'Original Data')
    for model in models:                      
        y_estimated = np.polyval(model,x)
        degree = len(model) - 1  
        rsquared = r_squared(y, y_estimated)
        
        if len(model) == 2:            
            slope = se_over_slope(x, y, y_estimated, model)
            pylab.plot(x, y_estimated, label = f'{degree} degree Model, R2={rsquared:.02}, SEoS={slope:.02}')
        else:
            pylab.plot(x, y_estimated, label = f'{degree} degree Model, R2={rsquared:.02}')
       
        pylab.ylabel('Degrees Celsius')
        pylab.xlabel('Years')
    pylab.title(title)
    pylab.legend(loc = 4)
    pylab.show()    
    

#x = np.array([1,2,3,4,5,6,7])
#y = np.array([3,7,9,17,20,11,15])
#models = generate_models(x,y,np.array([1,2,3,4]))
#evaluate_models_on_training(x,y,models)


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """       
    ## TAKE ALL CITIES       
    cities_averages = []
    
    ## FOR ALL CITIES, RETURN AVERAGE OS THE YEARS AND APPEND TO A LIST CONTAINING ALL CITIES
    for city in multi_cities:
        result_years = [climate.get_yearly_temp(city, year) for year in years]        
        cities_averages.append(np.array([np.mean(year) for year in result_years]))           

    ## RETURN SUM OF ELEMENTS (NP.ARRAY SUMS EACH POSITION) / LEN OF ARRAY = AVERAGE OF ALL CITIES    
    cities_averages = np.array(cities_averages)
    if len(multi_cities) == 1:        
        return cities_averages[0]
    else: 
        return sum(cities_averages) / len(cities_averages)     
    
    

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_average = []
    
    for i in range(1, len(y)+1):
        if i < window_length:
            moving_average.append(np.mean(y[0:i]))
        else:
            moving_average.append(np.mean(y[i-window_length:i]))
    
    return np.array(moving_average)
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return math.sqrt(float(sum((y - estimated) ** 2)) / len(y))    
    

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """        
    ## TAKE ALL CITIES          
    national_averages = []
    
    ## FOR ALL YEARS, TAKE EACH CITY AND PUT IN TO A LIST THE RESULTS FOR THE YEAR. THEN WITH ALL THE CITIES IN THE LIST, CALCULATE AVERAGES, APPEND TO NATIONAL AVERAGES, GO TO NEXT YEAR.   
    for year in years:
        cities_averages = []
        for city in multi_cities:        
            temp_year_city = climate.get_yearly_temp(city, year)    
            cities_averages.append(np.array(temp_year_city))  
        if len(cities_averages) == 1:        
            national_averages.append(cities_averages[0])
        else: 
            national_averages.append(sum(cities_averages) / len(cities_averages)) 
    
    ## CALCULATE STD FOR NATIONAL AVERAGES IN EACH YEAR
    return np.array([np.std(nat_std) for nat_std in national_averages])
    

def evaluate_models_on_testing(x, y, models, title='Degrees Celsius Over the Years'):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    ## PLOTTING ALL THE MODELS TO THE SAME GRAPH AS I DON'T HAVE TO DELIVER THE PSET. DOING IT TO SEE THE RESULTS, BUT I DON'T NEED TO FOLLOW ALL THE REQUIREMENTS.
    pylab.figure()
    pylab.plot(x, y, 'o', label = 'Original Data')
    for model in models:                      
        y_estimated = np.polyval(model,x)
        degree = len(model) - 1  
        rmse_result = rmse(y, y_estimated)           
        
        pylab.plot(x, y_estimated, label = f'{degree} degree Model, RMSE={rmse_result:.02}')       
        pylab.ylabel('Degrees Celsius')
        pylab.xlabel('Years')
    pylab.title(title)
    pylab.legend(loc = 'best')
    pylab.show()    
    

if __name__ == '__main__':   

    # Part A.4    
    ## INSTANTIATE A CLIMATE OBJECT TO USE DATA
    climate_obj = Climate('data.csv')
    
    ## LIST OF RESULTS OF APPLYING THE FUNCTION
    result = [climate_obj.get_daily_temp('New York'.upper(), 1, 10, date) for date in TRAINING_INTERVAL]   
    
    ## GENERATE MODEL AND PLOT RESULTS
    model = generate_models(TRAINING_INTERVAL, result, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, result, model)    
    
    
    ## SAME THING, BUT FOR YEARLY DATA
    result_years = [climate_obj.get_yearly_temp('New York'.upper(), year) for year in TRAINING_INTERVAL]    
    average_years = [np.mean(year) for year in result_years]
    model_years = generate_models(TRAINING_INTERVAL, average_years, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, average_years, model_years)    


## 1. What difference does choosing a specific day to plot the data for versus calculating the yearly average have on our graphs (i.e., in terms of the R2 values and 
## the fit of the resulting curves)? Interpret the results.
##   
## - Calculating the yearly average has a better R2 and fits better in the curve. Thats because more extreme values are atenuated when there are more data to use (more days)
##
## 2. Why do you think these graphs are so noisy? Which one is more noisy?
##    
## - The main reason is because the standard y axis for the graph, especially in the yearly data, is not from 0 to max_value... giving the impression of being more noisy.
## But also, temperatures are not stable in the same periods of different years, there's a substantial standard deviation there.
## The yearly one is less noisy because takes the average for the year, giving less importance to extreme values that might happen.
##
## 3. How do these graphs support or contradict the claim that global warming is leading to an increase in temperature? The slope and the standard error-to-slope ratio 
## could be helpful in thinking about this. 
##
## - Looking only at these graphs, we see a clear upward trend, and a < 0.5 Se/slope for the yearly graph (thats more reliable for this analysis). 
## But R2 is not high and that should be considerer and taken with caution.


    # Part B
    ## USING THE FUNCTION gen_cities_avg AND APPLYING MODEL JUST LIKE A.4 BUT FOR ALL CITIES
    cities_averages = gen_cities_avg(climate_obj, CITIES, TRAINING_INTERVAL)
    model_cities_years = generate_models(TRAINING_INTERVAL, cities_averages, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, cities_averages, model_cities_years)  


## 1. How does this graph compare to the graphs from part A (i.e., in terms of the R2 values, the fit of the resulting curves, and whether the graph supports/contradicts 
## our claim about global warming)? Interpret the results.
##
## - R2 values way higher, curve showing a higher upward tendency, SE/Slope very low, all poiting to more definitive results of the trend (rising temperature over the years in USA).
## we still need to be cautious because we are testing on training data, and in that case a high R2 does not necessarily mean we can predict the future with a different data set,
## it only means we are fitting better a straight line to the data at hand (but its looking better than before).
##
## 2. Why do you think this is the case?
##
## - More cities means more data, no cherrypicking a single city that might have discrapancies, and overall having less deviation on the observations.
##
## 3. How would we expect the results to differ if we used 3 different cities? What about 100 different cities?
##
## - Probably in 3 different cities the results would have been less statistically significant and in 100 different cities more significant, with the caveat that if you choose cities not 
## randomly, you can have a worse result with more cities
##
## 4. How would the results have changed if all 21 cities were in the same region of the United States (for ex., New England)? 
##
## - It would change because if cities are not chosen at random, you would see a lot of bias towards higher or lower temperatures


    # Part C
    ## USING THE FUNCTION gen_cities_avg AND APPLYING MODEL JUST LIKE A.4 BUT FOR ALL CITIES AND USING TEMPERATURES WITH MOVING AVERAGES
    cities_averages = gen_cities_avg(climate_obj, CITIES, TRAINING_INTERVAL)
    moving_averages_5y = moving_average(cities_averages, 5)
    model_cities_moving_avgs5 = generate_models(TRAINING_INTERVAL, moving_averages_5y, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, moving_averages_5y, model_cities_moving_avgs5)     


## 1. How does this graph compare to the graphs from part A and B (i.e., in terms of the R2 values, the fit of the resulting curves, and whether the graph supports/contradicts 
## our claim about global warming)? Interpret the results.
## Why do you think this is the case?  
##
## - It gets even better and trustworthy results than only with all cities but yearly data. Using moving averages, outliers becames even more atenuated and data more consistant.
## - With a 92% R2, the line is showing an even cleaner trend and Se/slope of 0.042 means that is far from a random result.
 

    # Part D.2
    ##SAME DATA AND MOVING AVERAGES FROM PART C ALREADY COMPUTED
    model_cities_partd = generate_models(TRAINING_INTERVAL, moving_averages_5y, [1,2,20])
    evaluate_models_on_training(TRAINING_INTERVAL, moving_averages_5y, model_cities_partd)      
    
## 1. How do these models compare to each other?
##
## - Higher Degrees fits better the data, with a higher R2 (thats normal on a training data set, because of overfitting)
##
## 2. Which one has the best R? Why?
##
## - The 20 degree model, because it tends to fit better all the data including the noise.
##
## 3. Which model best fits the data? Why? 
##
## - 20 degree model fits better on this training data set, but that doesn't mean its better for predictions
    
    cities_averages_testing = gen_cities_avg(climate_obj, CITIES, TESTING_INTERVAL)
    moving_averages_5y_testing = moving_average(cities_averages_testing, 5)
    evaluate_models_on_testing(TESTING_INTERVAL, moving_averages_5y_testing, model_cities_partd)
    
    ## MODEL OF PART A
    evaluate_models_on_testing(TESTING_INTERVAL, moving_averages_5y_testing, model_years)


## 1. How did the different models perform? How did their RMSEs compare?
##
## - This time, the more degrees on the model, the higher RMSE and inversely correlated with better results. 1 degree model shows a better RMSE and fits better with real data (predicts better).
##
## 2. Which model performed the best? Which model performed the worst? Are they the same as those in part D.2.I? Why? 
##
## - 1 degree model performed best and 20 degree worst. They are opposite do part d.2, because 20 degree fits too much to the noise, and 1 degree while less complex, get the trend better.
##
## 3. If we had generated the models using the A.4.II data (i.e. average annual temperature of New York City) instead of the 5-year moving average over 
## 22 cities, how would the prediction results 2010-2015 have changed? 
##
## - Would be way off, because NYC has a lower temperature than average US, predicting > 4º below what it should have for all the years.

    # Part E
    national_std = gen_std_devs(climate_obj, CITIES, TRAINING_INTERVAL)
    moving_averages_std = moving_average(national_std, 5)
    model_national_std = generate_models(TRAINING_INTERVAL, moving_averages_std, [1])
    evaluate_models_on_training(TRAINING_INTERVAL, moving_averages_std, model_national_std, 'STANDARD DEVIATION OF TEMPERATURES OVER THE YEARS IN THE US')
    
    
## 1. Does the result match our claim (i.e., temperature variation is getting larger over these years)?
##
## - No. Standard deviations are lower over the years.
##
## 2. Can you think of ways to improve our analysis? 
##
## - First, I would try another degrees models (but probably would come to the same conclusion despite fitting better to the curve, because we can actually see the trend by eye)
## Also would try using the standard deviation for each city before averaging them all (don't know if it would matter). I would also see all the countries, because looking only at USA, we're
## incurring in the same problem as in part A of only looking at one city, but this time in a global perspective.