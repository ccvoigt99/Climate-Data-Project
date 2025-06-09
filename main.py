# This is the file where all your code will actually run. Put the functions in 
# `project_code.py` and import them here.

#%%
from project_code import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

files = [
        r"Datasets/madisonweather.csv", 
        r"Datasets/rapidcityweather.csv", 
        r"Datasets/jacksonweather.csv", 
        r"Datasets/albuquerqueweather.csv"
]

# %%

df = load_climate_data(files)


#%%

# This is my code for your `plot_total_90_degree_days` function. You're kinda 
# reinventing the wheel. 

X = (df
    .query("DailyMaximumDryBulbTemperature >= 90")
    .groupby("CITY")
    .agg({"DailyMaximumDryBulbTemperature": "count"})
    .reset_index()
)

fig,ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data = X,
    x="CITY", 
    y="DailyMaximumDryBulbTemperature", 
    palette='viridis',
    ax = ax
)

ax.set_title("Total Number of 90 Degree Days by Location, 2014-2024")

# %%

def number_90_days_lineplot(df, city, ax):
    sns.lineplot(
        data = df.query(f"CITY == '{city}'"),
        x = "YEAR",
        y = "DailyMaximumDryBulbTemperature",
        ax = ax
    )

    ax.set_title(f"Number of 90 Degree Days Per Year: {city}")
                

X = (df
        .query("DailyMaximumDryBulbTemperature >= 90")
        .assign(YEAR=df.DATE.dt.year)
        .groupby(["CITY", "YEAR"])
        .agg({"DailyMaximumDryBulbTemperature": "count"})
        .reset_index()
)
    

fig, ax = plt.subplots(2,2, figsize=(12, 12), sharey=True, sharex=True) 
cities = ['Madison, WI', 'Rapid City, SD', 'Jackson, MS', 'Albuquerque, NM']

number_90_days_lineplot(X, cities[0], ax[0,0])
number_90_days_lineplot(X, cities[1], ax[0,1])
number_90_days_lineplot(X, cities[2], ax[1,0])
number_90_days_lineplot(X, cities[3], ax[1,1])


X
# %%
