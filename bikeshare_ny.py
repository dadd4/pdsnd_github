# bikshare_ny.py
# Project to explore US bikeshare data.
# Queries user on command to select 1 of 3 cities and computes
# statistics based on the data.

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ["All", "January", "February", "March", "April", "May", "June"]
DAYS = ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply
                      no month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    no_city = True
    while no_city:
        city_in = input("Enter city to explore (chicago, new york city, washington): ")
        city = city_in.lower()
        filename = CITY_DATA.get(city, None)
        if filename:
            no_city = False
        else:
            print("Invalid city, try again")

    # get user input for month (all, january, february, ... , june)
    no_month = True
    while no_month:
        month_in = input("Enter month (%s): " % MONTHS)
        month = month_in.lower().title()
        if month in MONTHS:
            no_month = False
        else:
            print("Invalid month, try again")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    no_day = True
    while no_day:
        day_in = input("Enter day (%s): " % DAYS)
        day = day_in.lower().title()
        if day in DAYS:
            no_day = False
        else:
            print("Invalid day, try again")

    print('-'*40)
    return city, month, day
# end get_filters


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    str1 = ""
    str2 = ""
    str3 = ""
    if month != "All":
        str1 = month
    if day != "All":
        str2 = day
    if str1 or str2:
        str3 = "filtered by (%s, %s)" % (str1, str2)

    print("\nLoading data for %s %s" % (city, str3))
    start_time = time.time()
    if city in CITY_DATA.keys():
        chosen_city = CITY_DATA[city]
    else:
        print('%s is not available' % city)
        return None
    
    # load data file into a dataframe
    df = pd.read_csv(chosen_city)
    print("Read %d rows of data in %s" % (df.shape[0], chosen_city))
    print("Converting time columns ...")
    
    # convert the Start Time column to datetime    
    df['Start Time'] = pd.to_datetime(df['Start Time']) 

    # extract month and day of week from Start Time to create new columns
    # weekday_name is deprecated
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # make a new column to be used later
    df['start_hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    month = month.lower()
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

    # filter by day of week if applicable
    day = day.lower()
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    print("Data filtered down to %d rows" % df.shape[0])
    print("\nload_data took %0.2f seconds." % (time.time() - start_time))
    return(df)
# end load_data


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    count_months = df['month'].value_counts()
    month_name = MONTHS[count_months.idxmax()]
    print("%s: %d times" % (month_name, count_months.max()))


    # display the most common day of week
    count_days = df['day_of_week'].value_counts()
    print("%s: %d times" % (count_days.idxmax(), count_days.max()))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    count_hours = df['start_hour'].value_counts()
    print("hour %s: %d times" % (count_hours.idxmax(), count_hours.max()))


    print('-'*40)
# end time_stats


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    count_st_stations = df['Start Station'].value_counts()
    print("Most common start station: %s: %d times" %
          (count_st_stations.idxmax(), count_st_stations.max()))

    # display most commonly used end station
    count_end_stations = df['End Station'].value_counts()
    print("Most common end station: %s: %d times" %
          (count_end_stations.idxmax(), count_end_stations.max()))


    # display most frequent combination of start station and end station trip
    dfg = df.groupby(['Start Station', 'End Station'])
    most_common_trip = dfg.size().idxmax()
    ntimes = len(dfg.groups[most_common_trip])
    print("Most common trip: %s to %s: %d times" %
          (most_common_trip[0], most_common_trip[1], ntimes))
    
    print('-'*40)
# end station_stats


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    # Average travel time in minutes
    total_time_hours = df['Trip Duration'].sum() / 3600
    print("Total trip time: %0.2f hours" % total_time_hours)

    # display mean travel time
    avg_time_minutes = df['Trip Duration'].mean() / 60
    print("Average trip time: %0.2f minutes" % avg_time_minutes)

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
# end trip_duration_stats


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count by user type:")
    print(df['User Type'].value_counts().to_string())

    # Display counts of gender
    if city in ['new york city', 'chicago']:
        print("\nCount by gender:")
        print(df['Gender'].value_counts().to_string())

    # Display earliest, most recent, and most common year of birth
    if city in ['new york city', 'chicago']:
        print("\nEarliest birth year: %d" % df['Birth Year'].min())
        print("Most recent birth year: %d" % df['Birth Year'].max())
        birthyear_counts = df['Birth Year'].value_counts()
        print("Most common year: %d (%d times)" %
              (birthyear_counts.idxmax(), birthyear_counts.max()))
    

    print('-'*40)
# end user_stats


def show_raw_data(df):
    """Ask user about displaying 5 rows of raw data at a time.
       Continue until user answers no
    """
    nrows = df.shape[0]
    indx = 0
    nshow = 5
    cols = df.columns
    while indx <= nrows-nshow:
        see_more = input('\nWould you like to see the raw data (5 rows)? Enter yes or no: ')
        if see_more == 'no':
            break
        else:
            rowdata = df.iloc[indx:indx+nshow]
            # make the displayed end time format consistent with start time
            rowdata['End Time'] = pd.to_datetime(rowdata['End Time'])
            for m in range(0, nshow):
                row = rowdata.iloc[m]
                print("\n'': \t\t{}".format(row[0]))
                for i in range(1, len(cols)):
                    print("{}:\t{}".format(cols[i], row[i]))

            indx += 5
# end show_raw_data


def main():
    """Main routine
    """
    while True:
        try:
            city, month, day = get_filters()
            #city = 'new york city'
            #month = 'all'
            #day = 'all'
            df = load_data(city, month, day)

            show_raw_data(df)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except KeyboardInterrupt:
            print("\n*** Received keyboard interrupt, exit")
            break

if __name__ == "__main__":
	main()
