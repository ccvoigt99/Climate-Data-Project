#Project 3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#First, I want to import my data and merg the four csvs into one dataframe
files = [r"C:\Users\cvoig\Box\718\data\madisonweather.csv", r"C:\Users\cvoig\Box\718\data\rapidcityweather.csv", r"C:\Users\cvoig\Box\718\data\jacksonweather.csv", r"C:\Users\cvoig\Box\718\data\albuquerqueweather.csv"]

def import_data(filepaths):
    
    dataframes = [pd.read_csv(fp, parse_dates=['DATE'], dtype={'NAME': str}) for fp in filepaths]
    return dataframes

dfs = import_data(files)
merged_df = pd.concat(dfs, ignore_index=True)

merged_df = merged_df.drop(columns=['LATITUDE', 'LONGITUDE', 'ELEVATION', 'REPORT_TYPE', 'SOURCE']) #Drop unnecessary columns
merged_df.dropna() # Drop rows with any NaN values

merged_df['NAME'].unique() # Checking the location names in the Name column

merged_df = merged_df[merged_df['NAME'] != 'JACKSON HAWKINS FIELD, MS US'] #dropping the redundant Jackson MS location

#Now that I have the data imported and merged, I want to plot the number of 90 degree days for each location

merged_df['YEAR'] = merged_df['DATE'].dt.year # Adding a year column to sum the number of 90 degree days by year

names = {
    'MADISON DANE CO REGIONAL AIRPORT, WI US': 'Madison, WI',
    'RAPID CITY REGIONAL AIRPORT, SD US': 'Rapid City, SD',
    'JACKSON INTERNATIONAL AIRPORT, MS US': 'Jackson, MS',
    'ALBUQUERQUE INTERNATIONAL AIRPORT, NM US': 'Albuquerque, NM'
}

merged_df['NAME'] = merged_df['NAME'].replace(names) #I also want to replace the airport names with the city names

def plot_total_90_degree_days(merged_df):
    
    locations = merged_df['NAME'].unique()
    total_counts = []

    for location in locations:

        count = merged_df[(merged_df['NAME'] == location) & (merged_df['DailyMaximumDryBulbTemperature'] >= 90)].shape[0]
        total_counts.append((location, count))

    total_counts_df = pd.DataFrame(total_counts, columns=['Location', 'Total 90 Degree Days'])
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=total_counts_df, x='Location', y='Total 90 Degree Days', palette='viridis')
    plt.title('Total Number of 90 Degree Days by Location, 2014-2024')
    plt.xlabel('Location')
    plt.ylabel('Total 90 Degree Days')
    plt.tight_layout()
    plt.show()

#plot_total_90_degree_days(merged_df) to view the plot

#LOCATIONS:
# 'Madison, WI'
# 'Rapid City, SD'
# 'Jackson, MS'
# 'Albuquerque, NM'

def plot_90_degree_days_by_year(merged_df, location):
   
    df_loc = merged_df[(merged_df['NAME'] == location) & (merged_df['DailyMaximumDryBulbTemperature'] >= 90)]
    
    yearly_counts = df_loc.groupby('YEAR').size().reset_index(name='90_degree_days')
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=yearly_counts, x='YEAR', y='90_degree_days', marker='o')
    plt.title(f'Number of 90 Degree Days Per Year: {location}')
    plt.xlabel('Year')
    plt.ylabel('Number of 90 Degree Days')
    plt.tight_layout()
    plt.show()

#plot_90_degree_days_by_year(merged_df, 'location') to view the plot for a location

#Now I calculate the mean and standard deviation of the RH for each location:

mean_table = merged_df.groupby('NAME')['DailyAverageRelativeHumidity'].mean().reset_index()
mean_table.columns = ['Location', 'RH Mean']

sd_table = merged_df.groupby('NAME')['DailyAverageRelativeHumidity'].std().reset_index()
sd_table.columns = ['Location', 'RH Standard Deviation']
summary = pd.merge(mean_table, sd_table, on='Location')

order = ['Madison, WI', 'Rapid City, SD', 'Jackson, MS', 'Albuquerque, NM']
summary = summary.set_index('Location').loc[order].reset_index()

#print(summary) to see the table

#Now, I plot the standard deviation of the RH, and number of 90 degree days for each location on a dual-axis graph:

def plot_rhstd_90_degree_days_df(merged_df, location):
   
    df_loc = merged_df[(merged_df['NAME'] == location) & (merged_df['DailyMaximumDryBulbTemperature'] >= 90)]
    yearly_counts = df_loc.groupby('YEAR').size().reset_index(name='90_degree_days')
    yearly_rhstd = df_loc.groupby('YEAR')['DailyAverageRelativeHumidity'].std().reset_index(name='rh_std')

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of 90 Degree Days', color='tab:blue')
    ax1.plot(yearly_counts['YEAR'], yearly_counts['90_degree_days'], marker='o', color='tab:blue', label='90 Degree Days')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('RH Standard Deviation', color='tab:red')
    ax2.plot(yearly_rhstd['YEAR'], yearly_rhstd['rh_std'], marker='s', color='tab:red', label='RH Std Dev')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(f'RH Std Dev & Number of 90 Degree Days Per Year: {location}')
    fig.tight_layout()
    plt.show()

#plot_rhstd_90_degree_days_df(merged_df, 'location') to view the plot for a location

#A table to examine the correlations
locations = merged_df['NAME'].unique()
correlations = []

for location in locations:

    df_loc = merged_df[(merged_df['NAME'] == location) & (merged_df['DailyMaximumDryBulbTemperature'] >= 90)]
    yearly = df_loc.groupby('YEAR').agg(
        num_days=('DailyMaximumDryBulbTemperature', 'count'),
        rh_std=('DailyAverageRelativeHumidity', 'std')
    ).reset_index()
    corr = yearly['num_days'].corr(yearly['rh_std'])
    correlations.append({'Location': location, 'Correlation': corr})

corr_df = pd.DataFrame(correlations)

#print(corr_df) to see the correlation table