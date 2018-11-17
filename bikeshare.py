import time
import pandas as pd
import numpy as np


#define dictionaries and lists for filter parameters
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

LOCALES = ['chicago', 'new york city', 'washington']

MONTHS = ['january', 'february','march', 'april', 'may', 'june']

WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) locale - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
       

    # add a nice little aesthetic pause as the program gets going :)
    time.sleep(1)

    # get the user's input for filtering by locale, month, day of week

    while True:
        locale = input('\nPlease select a city (Chicago, New York City, or Washington\n: ').lower()
        if locale in LOCALES:
            break
        else:
            print('No valid city/locale selected! Please try again.')


    month = input('\nPlease specify a month (January -- June) with which to filter data (enter "all" for no month filter)\n: ').lower() 

    day = input('\nPlease specify a day of week (Monday -- Sunday) with which to filter data (enter "all" for no day filter\n: ').lower()

    print('%'*40)

    return locale, month, day



def load_data(locale, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) locale - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data from from the locale specified in the get_filters() function
    df = pd.read_csv(CITY_DATA[locale])

    # clean up the time formatting for data filtering
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #add additional columns
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #filter by month as necessary or ignore the month filter
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[ df['month'] == month]

    #filter by day as necessary or ignore the day filter
    if day != 'all':
        df = df[ df['weekday'] == day.title()]


    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    # display the most common weekday
    most_common_weekday = df['weekday'].value_counts().idxmax()
    print("Most common weekday travel occurred on: ", most_common_weekday)

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common starting hour is: ", most_common_start_hour)

    print("\nThat took %s seconds to calculate!!" % (time.time() - start_time))

    print('%'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("Most common starting station was: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("Most common ending stations was: ", most_common_end_station)


    # display most frequent combination of start station and end station trip
    most_common_start_and_end = df[['Start Station', 'End Station']].mode().loc[0]
    print("Most common start and end station: {}, {}".format(most_common_start_and_end[0], most_common_start_and_end[1]))


    print("\nThat took %s seconds to calculate!!" % (time.time() - start_time))
    
    print('%'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total time traveled: ", total_travel_time)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("Average time traveled: ", avg_travel_time)


    print("\nThat took %s seconds to calculate!!" % (time.time() - start_time))
    
    print('%'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of distinct types of users: ")
    distinct_users = df['User Type'].value_counts()

    
    for index, user in enumerate(distinct_users):
        print(" {}: {}\n".format(distinct_users.index[index], user))

    # Display counts of gender
    print("Number of riders by gender: ")

    # add logic to account for Washington's data file not containing gender data
    if 'Gender' in df.columns:
        distinct_gender = df['Gender'].value_counts()
        for index, gender in enumerate(distinct_gender):
            print(" {}: {}".format(distinct_gender.index[index], gender))
    else:
        print("\nThere is no gender data available for the selected locale!\n")


   
    # Display earliest, most recent, and most common year of birth

    # add logic to account for Washington's data file not containing birth date data

    
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year']
        earliest_birth_year = birth_year.min()
        print("Earliest birth year was: ", earliest_birth_year)

        latest_birth_year = birth_year.max()
        print ("Latest birth year was:", latest_birth_year)

        common_birth_year = birth_year.value_counts().idxmax()
        print("Most common birth year was: ", common_birth_year)
    else:
        print("\nThere is no birth date data available for the selected locale!\n")

    


    print("\nThat took %s seconds to calculate!!" % (time.time() - start_time))
    
    print('%'*40) 


# Originally forgot to write a function that displays raw data to the user.
def print_data(df):
    """Prints lines of raw data at the request of the user (input)

    Args: dataframe/datafile as defined in earlier function
    
    Returns: null -- just prints out the requested data
    """

    print("\nData number crunching complete! The program can now display raw data samples upon request.\n")

    data_request = input("\nWould you like to see some raw data now? ('y' or 'n')\n: ")

    data_range = 0

    while True:
        if data_request is 'y':
            data_range += 5
            print(df.iloc[:data_range])
            data_request = input("\nWould you like to see 5 more rows of raw data? ('y' or 'n')\n: ")
        elif data_request is 'n':
            print("\nAlright, not going to show any raw data...\n")
            break
        else:
            data_request = input("\nPlease enter a 'y' or 'n'\n: ")




def main():
    while True:
        locale, month, day = get_filters()
        df = load_data(locale, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
