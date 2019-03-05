import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    msg = (
        '\nWhich City would you like to analyze?\n New York City, Chicago or Washington?\n: '
    )
    city = input(msg).lower()

    while city not in ['chicago', 'new york city', 'washington']:
        print('Invalid input')
        city = input(msg).lower()


    msg = (
        'What month do you want to analyze? Please enter a number 1-6 that corresponds to a month: \n'
        'january, february, march, april, may, june, if all 6 months press 7\n'
    )

    month = int(input(msg))

    while month < 1 or month > 7:
        month = int(input('Invalid number\n' + msg))

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = months[month-1]


    msg = ('Please enter a number 1-7 for the day of the week to be anaylyzed e.g 1=sunday, if all days press 8\n')
    day = int(input(msg))

    while day < 0 or day > 8:
        day = int(input('Invalid number\n' + msg))

    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',  'all']
    day = days[day-1]
    print('City: {}, Month: {}, Day of week: {}'.format(city, month, day))
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def view_raw_data(df):
    '''
    Shows raw data from Data Frame object

    Args:
        (DataFrame) A Panda's Data Frame object

    Returns:
        No return value
    '''

    choice = input('\nWould you like to see view data? Enter yes or no.\n')
    if choice.lower() == 'no':
        return

    tracker = 1
    for label, content in df.iterrows():
        print('label', label)
        print('Content', content)
        tracker += 1

        if tracker % 5 == 0:
            choice = input('Would you like to view 5 more views? Enter yes or no.\n')
            if choice.lower() == 'no':
                return

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()
    print('Most populay day of week: {}'.format(popular_day[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts()[0]
    print('Most popular start station: {}, Count: {}'.format(popular_start, count))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    count = df['End Station'].value_counts()[0]
    print('Most popular end station: {}, Count: {}'.format(popular_end, count))

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'].map(str) + ' - ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    count = df['Trip'].value_counts()[0]
    print('Most popular trip: {}, Count: {}'.format(popular_trip, count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_count = df['Trip Duration'].count()
    print('Total duration: {}, Total count: {}'.format(total_duration, total_count))

    # display mean travel time
    avg_duration= df['Trip Duration'].mean()
    print('Avg trip duration: {}'.format(avg_duration))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    # Display counts of user types\
    print('Subscriber count: {}'.format(user_types[0]))
    print('Customer count: {}'.format(user_types[1]))

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Male count: {}'.format(gender[0]))
        print('Female count: {}'.format(gender[1]))
    else:
        print('No gender data available')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
            oldest_birth = df['Birth Year'].min()
            recent_birth = df['Birth Year'].max()
            most_comm_birth = df['Birth Year'].mode()

            print('Earliest birth: {}'.format(oldest_birth))
            print('Most recent birth: {}'.format(recent_birth))
            print('Most common birth: {}'.format(most_comm_birth[0]))
    else:
            print('No birth data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
