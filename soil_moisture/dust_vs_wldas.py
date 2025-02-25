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

for date in dust_df['Date (YYYYMMDD)']:
    
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
        wldas_file = "WLDAS/WLDAS_NOAHMP001_DA1_20200102.D10.nc"
        wldas_ds = xr.open_dataset(wldas_file)
        print(wldas_ds)

