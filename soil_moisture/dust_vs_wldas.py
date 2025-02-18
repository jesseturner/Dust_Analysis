# Dust climatology compared to WLDAS soil moisture
## Use soil_moisture environment

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np

#--- Read dust data into a dataframe
file_path = '../dust_dataset_final_20241226.txt'
df = pd.read_csv(file_path, sep=r'\s+', skiprows=2, header=None)
df.columns = [
    'Date (YYYYMMDD)','start time (UTC)','latitude','longitude','Jesse Check'
]
print(df.head())

