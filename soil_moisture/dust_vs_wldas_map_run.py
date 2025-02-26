# Animation of WLDAS soil moisture with dust plumes added
## Use soil_moisture environment

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import subprocess
import os
from datetime import date, timedelta

#--- Read dust data into a dataframe
file_path = '~/Dust_Analysis/dust_dataset_final_20241226.txt'
dust_df = pd.read_csv(file_path, sep=r'\s+', skiprows=2, header=None)
dust_df.columns = [
    'Date (YYYYMMDD)','start time (UTC)','latitude','longitude','Jesse Check'
]
print(dust_df.head())

#--- Run the WLDAS imagery

year = 2001  # Change this to any desired year
start_date = date(year, 1, 2)
end_date = date(year, 12, 31)

current_date = start_date
while current_date <= end_date:
    YYYY = f"{current_date.year}"
    MM = f"{current_date.month:02d}"
    DD = f"{current_date.day:02d}" 
    current_date += timedelta(days=1)
    date = YYYY+MM+DD

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
    soil_moist = wldas_ds.SoilMoi00_10cm_tavg
    
    #--- Plot WLDAS data
    projection=ccrs.PlateCarree(central_longitude=0)
    fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})

    #levels = np.linspace(np.min(soil_moist), np.max(soil_moist), 31)

    c=ax.contourf(soil_moist.lon, soil_moist.lat, soil_moist, extend='both')
    clb = plt.colorbar(c, shrink=0.4, pad=0.02, ax=ax)
    clb.ax.tick_params(labelsize=15)
    clb.set_label('', fontsize=15)
    #ax.set_extent([longitude_west, longitude_east, latitude_south, latitude_north], crs=ccrs.PlateCarree())

    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(feature.STATES, zorder=100, edgecolor='#000', facecolor='none', linewidth=0.5)

    fig.savefig("WLDAS_maps/"+YYYY+"_"+MM+"_"+DD, dpi=200, bbox_inches='tight')
 
    plt.close()
