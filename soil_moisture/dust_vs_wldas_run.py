# Dust climatology compared to WLDAS soil moisture
## Use soil_moisture environment

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import subprocess
import os
from datetime import datetime

#--- Read dust data into a dataframe
file_path = '~/Dust_Analysis/dust_dataset_final_20241226.txt'
dust_df = pd.read_csv(file_path, sep=r'\s+', skiprows=2, header=None)
dust_df.columns = [
    'Date (YYYYMMDD)','start time (UTC)','latitude','longitude','Jesse Check'
]
print(dust_df.head())

for index, row in dust_df.iterrows():
    date = row['Date (YYYYMMDD)']
    latitude = row['latitude']
    longitude = row['longitude']

    date_obj = datetime.strptime(str(date), "%Y%m%d")
    YYYY = date_obj.strftime("%Y")
    MM = date_obj.strftime("%m")
    DD = date_obj.strftime("%d")

    #--- Check if WLDAS file already exists
    file_name = f"WLDAS_NOAHMP001_DA1_{YYYY}{MM}{DD}.D10.nc"
    if os.path.exists("WLDAS/"+file_name):
        print("Already downloaded for ", date)
    else:
        print("Downloading", date, "data...")

    #--- Download WLDAS data if necessary
        subprocess.run(["bash", "wldas_data_download.sh", str(date)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    #--- Read WLDAS data
    wldas_ds = xr.open_dataset("WLDAS/"+file_name)

    #--- Filter to near dust event
    lat_max = float(latitude)+1
    lat_min = float(latitude)-1
    lon_max = float(longitude)+1
    lon_min = float(longitude)-1
    wldas_ds_subset = wldas_ds.sel(lat=slice(lat_max, lat_min), lon=slice(lon_min, lon_max))
    wldas_ds_averaged = wldas_ds_subset.mean(dim=['time', 'lat', 'lon'])

    #--- Save or append values to CSV file
    averaged_values = {var: wldas_ds_averaged[var].values for var in wldas_ds_averaged.variables}
    df = pd.DataFrame(averaged_values, index=wldas_ds_subset['time'].values)

    csv_file = 'averaged_data.csv'
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False) 
