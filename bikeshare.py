import time
import pandas as pd
import numpy as np

cities=['chicago','new york city','washington']
months=['all','january','february','march','april','may','june']
days=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        #convert user input to lowercase
        city=input("Which city's data do you want to explore? (Chicago,New York City,Washington)\n").lower()
        if city in cities:
            break
        else:
            print("\nInvalid City"+"!"*5)
            print("One of the following cities are valid entries:\n Chicago\n New York City\n Washington")
    # get use input whether to filter data by month and day or the week or not
    print('\n Do you want to filter data by month and day of the week?')
    filter=input('Yes or No')
    if filter.lower()=='no':
        month='all'
        day='all'
        return city, month, day
    # get user input for month (all, january, february, ... , june). Using loop to handle invalid inputs
    while True:
        print("\nDo you want to look at all months data or only one month? (Type 'all' for all months or type month's name)")
        month=input("Valid months are january to june ").lower() #convert user input to lowercase
        if month in months:
            break
        else:
            print("\nInvalid Input for month"+"!"*5)
            print("Valid inputs are 'all' and months from january to june")

    # get user input for day of week (all, monday, tuesday, ... sunday). Using loop to handle invalid inputs
    while True:
        print("\nDo you want to look at all days data or only one specific day? (Type 'all' for all months or type day's name)")
        day=input("Valid day input are monday to sunday ").lower() #convert user input to lowercase
        if day in days:
            break
        else:
            print("\nInvalid Input for day"+"!"*5)
            print("Valid inputs are 'all' and days from monday to sunday")

    print("Following are the parameters for data:\nCity: {} \nMonth: {}\nDay: {}".format(city.title(),month.title(),day.title()))

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
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day=days.index(day)-1
        df = df[df['day_of_week']==day]
    print(df['day_of_week'].mode()[0])
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month=df['month'].mode()[0]
    common_month=months[common_month].title() #get month string
    print("Busiest month was {}.".format(common_month))

    # display the most common day of week
    common_day=df['day_of_week'].mode()[0]
    print("Day= ",common_day)
    common_day=days[common_day+1].title() # get day string
    print("Busiest day of the week was {}".format(common_day))

    # display the most common start hour
    df['Start Hour']=df['Start Time'].dt.hour # add 'Start Hour' column in Data Frame
    common_start_hour=df['Start Hour'].mode()[0]
    if common_start_hour<12:
        print("Commont start hour is {} a.m.".format(common_start_hour))
    else:
        if common_start_hour>12:
            common_start_hour-=12
        print("Common start hour is {} p.m.".format(common_start_hour))
    df.pop('month')
    df.pop('Start Hour')
    df.pop('day_of_week')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station=df['Start Station'].mode()[0].title()
    print("Bikes are picked up mostly from station at {}".format(common_start_station))

    # display most commonly used end station
    common_end_station=df['End Station'].mode()[0].title()
    print("Bikes are dropped off mostly at station at {}".format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['Station_combined']=df['Start Station']+'/'+df['End Station'] #combining address string
    common_route=df['Station_combined'].mode()[0].split('/') #spliting two address
    print("Most Frequent start and end station pair is:\n {} and {}.".format(str(common_route[0]),str(common_route[1])))
    df.pop('Station_combined')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time in hours
    total_travel_hours=round(df['Trip Duration'].sum()/3600,2)
    print("Total Travel time was {} hours.".format(total_travel_hours))
    # display mean travel time in minutes
    mean_travel_time=round(df['Trip Duration'].mean()/60,2) 
    print("Average travel time is: {} minutes".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count=df['User Type'].value_counts()
    print("Following is the count of user types")
    print_series(user_type_count)


    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count=df['Gender'].value_counts()
        print("Following is the count for Gender")
        print_series(gender_count)
    else:
        print("Gender Information Not Available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year=int(df['Birth Year'].min())
        recent_birth_year=int(df['Birth Year'].max())
        common_birth_year=int(df['Birth Year'].mode()[0])
        print("Youngest customer was born in year {}.".format(recent_birth_year))
        print("Oldest customer was born in year {}.".format(earliest_birth_year))
        print("Most common year of birth among customer was {}.".format(common_birth_year))
    else:
        print("Birth Year Information about customer not available.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_series(input_series):
    data=input_series.values
    indices=input_series.index
    for d,index in zip(data,indices):
        print("{}: {}".format(index,d))

def display_raw_data(df):
    """This function prints the 5 line of raw data from a
    data frame until user wants to stop it."""
    nxt=''
    start_row=0
    end_row=5
    while True:
        see_raw_data=input("Would you like to see {} 5 lines of raw data? Yes or No".format(nxt))
        nxt='next'
        if see_raw_data.lower()=='no':
            break
        print(df[start_row:end_row])
        start_row=end_row
        end_row+=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
