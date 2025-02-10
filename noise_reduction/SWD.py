#---Cloud search libraries
import s3fs
import requests
import fnmatch

#---Accessory libraries
import datetime
import xarray as xr
import netCDF4
import numpy as np
import os

#---My functions
import satellite_latlon_ABI as sat

def makeSWD(year, julian_day, month, day, hour, datetime_str, latitude_north, latitude_south, longitude_west, longitude_east):
    #---Connecting to AWS remote storage:
    fs = s3fs.S3FileSystem(anon=True)

    #---Search the AWS database
    bucket = 'noaa-goes16'
    product = 'ABI-L1b-RadF' #---Full disk ABI radiance
    band_13 = '13' #--- 10.3 um
    band_15 = '15' #--- 12.3 um
    data_path = bucket + '/' + product + '/'  + str(year) + '/' + julian_day + '/' + str(hour).zfill(2)
    files = fs.ls(data_path)
    files_band_15 = [file for file in files if fnmatch.fnmatch(file.split('/')[-1], 'OR_ABI-L1b-RadF-M6C' + band_15 + '*')]
    files_band_13 = [file for file in files if fnmatch.fnmatch(file.split('/')[-1], 'OR_ABI-L1b-RadF-M6C' + band_13 + '*')]
    file_15 = files_band_15[0] #---first is the top-of-the-hour
    file_13 = files_band_13[0]
    print(file_15)

    resp_15 = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+file_15[12:])
    if str(resp_15) != '<Response [200]>':
        print('b15 file not found in AWS servers')

    resp_13 = requests.get(f'https://'+bucket+'.s3.amazonaws.com/'+file_13[12:])
    if str(resp_13) != '<Response [200]>':
        print('b13 file not found in AWS servers')

    #---Open the satellite data:
    nc_15 = netCDF4.Dataset(file_15, memory = resp_15.content)
    ds_15 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_15))

    nc_13 = netCDF4.Dataset(file_13, memory = resp_13.content)
    ds_13 = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_13))

    #---Get the latitudes and longitudes
    ds_lat_lon_15 = sat.calc_latlon(ds_15)
    ((x1,x2), (y1, y2)) = sat.get_xy_from_latlon(ds_lat_lon_15, (latitude_south, latitude_north), (longitude_west, longitude_east))
    region_15 = ds_lat_lon_15.sel(x=slice(x1, x2), y=slice(y2, y1))

    ds_lat_lon_13 = sat.calc_latlon(ds_13)
    region_13 = ds_lat_lon_13.sel(x=slice(x1, x2), y=slice(y2, y1))

    #---Convert radiance to brightness temperature
    wl_15 = round(region_15.band_wavelength.values[0],1)
    wl_13 = round(region_13.band_wavelength.values[0],1)

    Tb_15 = (region_15.planck_fk2/(np.log((region_15.planck_fk1/region_15.Rad)+1)) - region_15.planck_bc1)/region_15.planck_bc2
    Tb_13 = (region_13.planck_fk2/(np.log((region_13.planck_fk1/region_13.Rad)+1)) - region_13.planck_bc1)/region_13.planck_bc2

    #---Create strings for the save file
    date_str = str(datetime_str).replace('-', '_').replace(' ', '_')

    #---Create and save the BTD
    BTD = Tb_15 - Tb_13
    save_dir = "swd_files"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  
    BTD.to_netcdf(save_dir+"/satellite_btd_"+date_str+".nc")

    return BTD
