import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as feature

#--- datetime must be in 2025_01_30_00Z format
#--- utc must be string in 00Z format

def make_adjusted(utc, latitude_north, latitude_south, longitude_west, longitude_east):
    swd_file = "swd_files/satellite_btd_2025_01_30_"+utc+".nc"
    swd_average_file = "monthly_average/2025_Jan_"+utc+".nc"

    SWD = xr.open_dataarray(swd_file)
    SWD_average = xr.open_dataarray(swd_average_file)

    SWD_adjusted = SWD - SWD_average
    
    save_dir = "swd_adjusted"
    SWD_adjusted.to_netcdf(save_dir+"/2025_01_30_"+utc+".nc")

    return SWD_adjusted