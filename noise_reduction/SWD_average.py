import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as feature
import glob

#--- utc must be string in 00Z format
def make_average(utc, latitude_north, latitude_south, longitude_west, longitude_east):
    
    #--- Set the range for the fig title
    start = "2025/01/01 "+utc
    end = "2025/01/31 "+utc

    save_name = "monthly_average/2025_Jan_"+utc

    #--- Get all files for a certain month and time
    file_paths = sorted(glob.glob("swd_files/satellite_btd_2025_01_??_"+utc+".nc"))

    #--- Open data and average over time range
    data_arrays = [xr.open_dataarray(file) for file in file_paths]
    combined = xr.concat(data_arrays, dim="datetime")
    median_data = combined.median(dim="datetime", skipna=True)

    #--- Add the latitudes and longitudes, which got removed due to datetime variable
    lat_median = combined.lat
    lon_median = combined.lon
    median_data = median_data.assign_coords(lat=lat_median, lon=lon_median)

    #--- Set negatives and NaNs to zero
    median_data = median_data.where(median_data >= 0, 0)
    median_data = median_data.fillna(0)

    #--- Save file
    median_data.to_netcdf(save_name+".nc")

    return median_data