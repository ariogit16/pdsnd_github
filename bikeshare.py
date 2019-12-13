import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS_LIST = ['all', 'january','february','march','april','may','june','july','august','september','october','november','december']
DAYS_LIST = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please type a city (Chicago, New York City, Washington): ")
            city = city.lower()
            if city in CITY_DATA.keys():
                print(">>Thank You\n")
                break
            else:
                print("...I'm sorry, was that Chicago, New York City, or Washington?\n")
        except vallueError:
            print("Invalid input, make sure you only enter the provided options\n")
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a month name (january, february, etc.) or all to view all months: ")
            month = month.lower()
            if month in MONTHS_LIST:
                print(">>Got it!\n")
                break
            else:
                print("...That didn't appear to be correct month name, type all for all months\n")
        except vallueError:
            print("Invalid input, make sure you only enter the provided options\n")
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter day of the week (monday, tuesday, etc.) or all to view all days: ")
            day = day.lower()
            if day in DAYS_LIST:
                print(">>Awesome!\n")
                break
            else:
                print("...That didn't appear to be a day of week, type all for all days\n")
        except vallueError:
            print("Invalid input, make sure you only enter the provided options\n")

    print("Your inputs were city={}, month={}, day={}.".format(city, month, day))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time & End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #create a new columnsfor Duration
    df['duration_t'] = df['End Time']- df['Start Time']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = MONTHS_LIST[1:]
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def display_raw(city):
    """Asks if user wants to view raw data based on their city selection"""
    # load data into datafile
    df = pd.read_csv(CITY_DATA[city])
    try:
        view = str(input("Would you like to view 5 lines of raw data of {} first?(Y/N) ".format(city.title()))).lower()
        if view == "y":
            print("\n")
            print(df.head(5))
            # set intial value for next set of data
            a=4

            while True:
                try:
                    view = str(input("Would you like to view 5 more?(Y/N)")).lower()
                    if view == "y":
                    # check if at end of data if not iterate upper bound
                        b = a + 6
                        print(df[a+1:b])
                        # move upper bound to lower bound -1
                        a = b-1
                        # check if upper bound reach the end of dataframe
                        # continue if not, get out if yes.
                        if b <= len(df):
                            continue
                        else:
                            print("That was the last 5 lines of data.")
                            break
                    elif view == "n":
                        break
                    else:
                        print("Y or y for yes and N or n for No.")
                except ValueError:
                    print("That's not the input I expected.")

    except ValueError:
        print("That's not the input I expected.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = MONTHS_LIST[df['month'].mode()[0]]
    print("The most common travel month is      --> {}".format(common_month.title()))
    # TO DO: display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print("The most common travel day is        --> {}".format(common_day.title()))

    # TO DO: display the most common start hour
    common_start = df['hour'].mode()[0]
    print("The most common travel start time is --> {}".format(common_start))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    s_station = df['Start Station'].mode()[0]
    print("The most popular start station is                    --> {}".format(s_station))

    # TO DO: display most commonly used end station
    e_station = df['End Station'].mode()[0]
    print("The most popular end station is                      --> {}".format(e_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + " to " + df['End Station']
    combine = df['Start End'].mode()[0]
    print("The most popular start station & end station trip is --> {}".format(combine))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['duration_t'].sum()
    print("The total travel time for is   --> {} days {} hours {} minutes".format(total_travel.days,total_travel.seconds//3600,(total_travel.seconds//60)%60))
    # TO DO: display mean travel time
    avg_travel = df['duration_t'].mean()
    print("The average travel time for is --> {} days {} hours {} minutes".format(avg_travel.days,avg_travel.seconds//3600,(avg_travel.seconds//60)%60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usr_typ_ls = dict(zip(df['User Type'].value_counts().index, df['User Type'].value_counts().values))
    for key,value in usr_typ_ls.items():
        print("There are {} {}(s)".format(value, key))
    # check for Gender column (because Washington.csv does not have one)
    if "Gender" in df.keys():
    # TO DO: Display counts of gender
        gender = dict(zip(df['Gender'].value_counts().index,df['Gender'].value_counts().values))
        for key,value in gender.items():
            if gender.items():
                print("There are {} {}(s)".format(value, key))
            else:
                break

    # TO DO: Display earliest, most recent, and most common year of birth
    # check for Birth Year because washington.csv does not have one
    if "Birth Year" in df.keys():
    # need to convert datatypes as each method returns different types
        print("\nThe earlierst year of birth is   --> {}".format(str(int(df['Birth Year'].min()))))
        print("The most recent year of birth is --> {}".format(str(int(df['Birth Year'].max()))))
        print("The most common year of birth is --> {}".format(str(int(df['Birth Year'].mode()[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #in case the data is empty
        if df.empty == False:
            display_raw(city)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print("There is no data to explore with your current selection")\

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
