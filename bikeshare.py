#!/usr/bin/env python
# coding: utf-8

# In[12]:


#import data into python, and set parent data sets
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

#define a function to get user input
def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        else:
            print(f"Invalid input, please choose from {valid_options}")
def user_input():
    print("Hello and welcome! Let's explore some selected US cities bikeshare data together!" )

    city = get_valid_input('Enter the city (Chicago, New York City, Washington): ', CITY_DATA)
    month = get_valid_input('Enter a valid month (all, January, February, ..., June): ', months)
    day = get_valid_input('Enter the day of the week (all, Monday, Tuesday,..., Sunday): ', weekdays)

    print('-'*80)
    return(city, month, day)

#define data frame to be used in subsequent functions
def load_data(city, month, day):
    city_file = CITY_DATA[city]
    df = pd.read_csv(city_file)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name().str.title()

    if month != 'all':
        df = df[df['Month'] == months.index(month)]
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    return df
    print('-'*80)
    print('Below, is a sample of the data you are about to analyse')
    print('\n')
    print(df.head(n=5).to_string(index=False))
    print('-'*80)

    return df #ensures that a preview is seen, and that the Dataframe is returned

#define a function to plot histograms
def plot_histogram(data, bins, title, xlabel, ylabel):
plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid(True)
#define a function to calculate and display basic time statistics
def basic_time_statistics(df):
    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()
    print(f"The most common month is : {months[df['Month'].mode()[0]]}")
    print(f"The most common day of the week is : {df['Day of Week'].mode()[0]}")
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    am_pm = 'AM' if common_hour < 12 else 'PM'
    common_hour = common_hour % 12 if common_hour % 12 != 0 else 12
    print(f"The most common start hour is: {common_hour:02d}:{df['Start Time'].dt.minute.mode()[0]:02d} {am_pm}")
    print('\n')
    #include histograms of basic statistics
    #Histogram of start times

# Example usage in basic_time_statistics():
    plot_histogram(df['Hour'], bins=range(0, 25, 2), title="Distribution of Start Times", xlabel="Hour of Day", ylabel="Count")
    plot_histogram(df['Day of Week'], bins=np.arange(len(days_order) + 1) - 0.5, title="Distribution of Weekdays", xlabel="Weekday", ylabel="Count")
    plot_histogram(df['Month'], bins=np.arange(1, len(months)+2) -0.5, title="Distribution of Months", xlabel="Month", ylabel="Count")

    plt.tight_layout
    plt.show()
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*80)

#define a function to calculate the most popular start stations and most popular trip
def station_statistics(df):
    print('\nCalculating the most popular stations and trips...\n')
    start_time = time.time()
    print(f"The most common start station is : {df['Start Station'].mode()[0]}")
    print(f"The most common end station is : {df['End Station'].mode()[0]}")
    print(f"The total number of unique start stations is : {df['Start Station'].unique().size}")
    print(f"The total number of unique end stations is : {df['End Station'].unique().size}")
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start and end station is : {common_trip[0]} to {common_trip[1]}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 80)

#define a function to calculate trip duration statistics, and display some of the information as a histogram
def trip_duration_statistics(df):
    print('\nCalculating statistics on trip durations...\n')
    start_time = time.time()
    print(f"The total travel time is : {int(df['Trip Duration'].sum() // 3600)} hours and {int((df['Trip Duration'].sum()  % 3600 ) // 60)} minutes")
    print(f"The mean travel time is: {int(df['Trip Duration'].mean() // 3600 )} hours and {int((df['Trip Duration'].mean() % 3600) //60)} minutes")
    print('\nHere are some more insights on the data :\n')
    duration_stats = df['Trip Duration'].agg(['min', 'max', 'median'])
    print(duration_stats)
    print("These values are in seconds, and may be difficult to read. They are simplifiedn to minutes below")
    print(f"The minimum trip duration in minutes is : {df['Trip Duration'].min()/60}")
    print(f"The maximum trip duration in minutes is : {df['Trip Duration'].max()/60}")
    print(f"The median trip duration in minuted is : {df['Trip Duration'].median()/60}")
    df['Trip Duration'].hist(grid=True, bins=10, backend=None, legend=True)
    plt.show()
    print('\n This took %s seconds.' % (time.time()-start_time))

def user_category_statistics(df):
    print('\nCalculating the user type and category statistics...\n')
    start_time = time.time()
    print('Counts of user types')
    print(df['User Type'].value_counts())
    print('\n')
    df['User Type'].hist(bins=3, legend=True)
    plt.show()
    print('\n')
    if 'Gender' in df.columns:
        print('\nCounts of gender are as follows:')
        print(df['Gender'].value_counts())
        print('\n')
        df['Gender'].hist(bins=3, legend=True)
        plt.show()
        gender_counts = df['Gender'].value_counts()
        gender_percentages = (gender_counts / gender_counts.sum()) * 100
        print(gender_percentages)
        print('\n')
    else:
          print("\nGender information is not available in the dataset.")

    if 'Birth Year' in df.columns:
        current_year = pd.to_datetime('today').year
        df['Age'] = current_year - df['Birth Year']
        bins = [0, 18, 26, 40, 60, np.inf]
        labels = ['Youth (0 to 18)', 'Young Adult (18 to 26)', 'Middle Aged (26 to 40)', 'Older Adult (40 to 60)', 'Senior Citizen (over 60)']
        df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right = False)
        user_group_statistics = df.groupby('Age Group').agg({
            'Trip Duration': ['count', 'sum', 'mean']
        })
        user_group_statistics.columns = ['Total Trips', 'Total Duration (s)', 'Average Duration (s)']
        user_group_statistics['Total Duration (h)'] = user_group_statistics['Total Duration (s)'] / 3600
        user_group_statistics['Average Duration (h)'] = user_group_statistics['Average Duration (s)'] / 3600

        print('\nBelow, is a breakdown of users into age categories:')
        print(user_group_statistics[['Total Trips', 'Total Duration (s)', 'Total Duration (h)']])
        print('\n', '-' * 80)
        print(user_group_statistics[['Average Duration (s)', 'Average Duration (h)']])
        print('\n')
        df['Age'].hist(bins=8, legend =True)
        plt.show()

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-' * 80)

#defining a function to show in an iterative way, 5 rows of data at a time
def show_raw_data(df):
    start = 0
    end = 5
    while True:
          show_data_input = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\nKindly note, any other answer besides yes or no will default to a no!\n')
          if show_data_input.lower() != 'yes':
              break

          else:
              data_subset = df.iloc[start:end]
              print(data_subset)
              start += 5
              end += 5
          if start>= len(df):
              print('No more raw data to display')
              break

#defining the main function that will call the other functions for input and data display
def main():
    while True:
          city, month, day = user_input()
          df = load_data(city, month, day)

          basic_time_statistics(df)
          station_statistics(df)
          trip_duration_statistics(df)
          user_category_statistics(df)

          show_raw_data(df)

          restart = input('\nWould you like to restart with a different selection? Enter yes or no. \nKindly note any other answer will default to no!\n')

          if restart.lower() !=  'yes':
              break

if __name__ == "__main__":
    main()
