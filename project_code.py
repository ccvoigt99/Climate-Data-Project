import pandas as pd


__DEFAULT_LOCATIONS__ = pd.DataFrame(
    [
        ['MADISON DANE CO REGIONAL AIRPORT, WI US', 'Madison, WI'],
        ['RAPID CITY REGIONAL AIRPORT, SD US', 'Rapid City, SD'],
        ['JACKSON INTERNATIONAL AIRPORT, MS US', 'Jackson, MS'],
        ['ALBUQUERQUE INTERNATIONAL AIRPORT, NM US', 'Albuquerque, NM'],
    ],

    columns=['NAME', 'CITY']
)



# This throws warnings. Fix that.
def load_climate_data(filepaths, locations = __DEFAULT_LOCATIONS__):
    
    # What columns do we actually need? Only load the ones you need
    columns = ["DATE", "NAME", "DailyMaximumDryBulbTemperature"]

    dataframes = [
        pd.read_csv(
            fp, 
            parse_dates=['DATE'], 
            dtype={'NAME': str},
            usecols=columns
            ) 
        for fp in filepaths
        ]
    
    df = (pd.concat(dataframes, ignore_index=True)
          .merge(locations, on='NAME', how='inner')
          .dropna()
    )

    return df