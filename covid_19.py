#Covid-19 statistics by country (current and total)
#Irene Moiseenko

import pandas as pd
import datetime
from datetime import date
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Data actualized from European Centre for Disease Prevention and Control
CSV_DATA = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
#CSV_DATA = 'COVID CSV'

COUNTRIES_NAMES1 = ["United_States_of_America", "Democratic_Republic_of_the_Congo",
                    "United_Kingdom", "United_Arab_Emirates"]
COUNTRIES_NAMES2 = ["USA", "DR Congo", "UK", "UAE"]
CASES_FIELD = 'cases'
DEATHS_FIELD = 'deaths'
COUNTRY_FIELD = 'countriesAndTerritories'
BARS_COLOR1 = 'crimson'
BARS_COLOR2 = 'maroon'

def main():
    print("In this application you can find Covid-19 current statistics per country.")
    user_selection = 6
    while user_selection < 0 or user_selection > 5:
        user_selection = int(input("Please enter a number 0, 1, 2 or 3:\n"
                                    "0 - Exit the program;\n"
                                    "1 - Show The Countries With The Highest New Covid-Cases;\n"
                                    "2 - Show The Countries With The Highest New Covid-Deaths;\n"
                                    "3 - Select a country to show DAILY Covid changes;\n"
                                    "4 - Select a country to show TOTAL cases and predictive modeling;\n"
                                    "5 - Select a country to show TOTAL deaths and predictive modeling.\n"))
    if user_selection == 0:
        exit()

    print("Please wait, the data is uploading.")
    #reading, sorting and cleaning data
    df = pd.read_csv(CSV_DATA)
    df = df.sort_values([COUNTRY_FIELD, 'year', 'month', 'day'])
    df = df.replace(COUNTRIES_NAMES1, COUNTRIES_NAMES2) #change some countries names for convenience
    todays_date_data = get_today_frame(df) #getting a date frame with today date

    while user_selection != 0:
        #The Countries With The Highest New Cases
        if user_selection == 1:
            top_cases = todays_date_data.nlargest(20, CASES_FIELD) #select 20 countries with highest cases
            create_top_chart(top_cases, CASES_FIELD, BARS_COLOR1)

        #The Countries With The Highest New Cases
        elif user_selection == 2:
            top_deaths = todays_date_data.nlargest(10, DEATHS_FIELD) #select 10 countries with highest deaths
            create_top_chart(top_deaths, DEATHS_FIELD, BARS_COLOR2)

        #Select a country to show DAILY Covid changes
        elif user_selection == 3:
            user_country = input("Enter a Country Name: ")
            country_frame = df[df[COUNTRY_FIELD] == user_country] #create a frame for a specific country
            create_country_plot(country_frame, user_country)

        #Select a country to show TOTAL cases and predictive modeling
        elif user_selection == 4:
            user_country = input("Enter a Country Name: ")
            country_frame = df[df[COUNTRY_FIELD] == user_country] #create a frame for a specific country
            predictive_modeling(country_frame, CASES_FIELD, user_country)

        #Select a country to show TOTAL deaths and predictive modeling.
        elif user_selection == 5:
            user_country = input("Enter a Country Name: ")
            country_frame = df[df[COUNTRY_FIELD] == user_country] #create a frame for a specific country
            predictive_modeling(country_frame, DEATHS_FIELD, user_country)

        user_selection = 6
        #repeat selection
        while user_selection < 0 or user_selection > 5:
            user_selection = int(input("Please enter a number 0, 1, 2 or 3:\n"
                                        "0 - Exit the program;\n"
                                        "1 - Show The Countries With The Highest New Covid-Cases;\n"
                                        "2 - Show The Countries With The Highest New Covid-Deaths;\n"
                                        "3 - Select a country to show DAILY Covid changes;\n"
                                        "4 - Select a country to show TOTAL cases and predictive modeling;\n"
                                        "5 - Select a country to show TOTAL deaths and predictive modeling.\n"))
#a frame with today statictics
def get_today_frame(df):
    today = date.today()
    today_date = today.strftime("%d/%m/%Y")
    today_frame = df[df['dateRep'] == today_date]
    return today_frame

def test():
    print("test")

def create_top_chart(top_frame, name_field, color_name):
    'create a bar-chart for countries with the highest volumes'
    x = top_frame[COUNTRY_FIELD]
    y = top_frame[name_field]
    plt.figure(figsize=(10, 5))
    plt.barh(x, width=y,  color=color_name)
    for index, value in enumerate(y):
        plt.text(value, index, str(value), fontsize=8, horizontalalignment='left', verticalalignment='center')
    today = date.today()
    today_date_US_format = today.strftime("%m/%d/%Y")
    plt.title('Countries with the highest new Covid-19 ' + name_field +', ' + today_date_US_format)
    plt.show()

#create a plot for selected country with daily cases and deaths
def create_country_plot(country_frame, user_country):
    x_dates_values = [datetime.datetime.strptime(d,"%d/%m/%Y").date() for d in country_frame['dateRep']]
    y_cases_values = country_frame['cases']
    y_deaths_values = country_frame['deaths']
    plt.plot(x_dates_values, y_cases_values, label="New Cases")
    plt.plot(x_dates_values, y_deaths_values, label="New Deaths")
    plt.legend(loc="upper left")
    plt.title('Covid-19 Statistics, ' + user_country)
    plt.ylabel('Cases/ Deaths')
    plt.xlabel('Date')
    plt.show()

#create an array with total cases / deaths for a specific country
def total_cases(country_frame, name_field):
    new_list = country_frame[name_field].to_list()
    total_cases_list = []
    previous_day = 0
    for i in range(len(new_list)):
        current_day = new_list[i]
        sum_cases = current_day + previous_day
        total_cases_list.append(sum_cases)
        previous_day = sum_cases
    numpy_array = np.array(total_cases_list)
    return numpy_array

#create a prediction
def predictive_modeling(frame, field_name, country):
    y = total_cases(frame, field_name)
    x = np.arange(len(y))
    plt.plot(x, y, 'ko', label='Total number of ' + field_name + ', ' + country)
    # Initialized with a p0 value to give a starting point for trial and error
    popt, pcov = curve_fit(func, x, y, p0=(1, 0.1))
    plt.plot(x, func(x, *popt), 'r-', label='fit: a = %5.3f, b = %5.3f' % tuple(popt))
    plt.xlabel('Days Since 12/31/2019')
    plt.ylabel('Total number of ' + field_name + ', ' + country)
    plt.legend()
    plt.show()

#Levenberg–Marquardt (LM) Algorithm
def func(x, a, b):
    return a * np.exp(b * x)

if __name__ == '__main__':
    main()