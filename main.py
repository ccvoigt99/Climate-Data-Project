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

