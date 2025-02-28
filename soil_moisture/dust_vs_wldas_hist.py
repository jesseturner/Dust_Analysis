# Dust climatology compared to WLDAS soil moisture
## Use soil_moisture environment

import pandas as pd
import os
import xarray as xr
import numpy as np
import re

#--- Create distribution for total WLDAS
data_dir = "WLDAS"
save_path_WLDAS_all = "histograms/WLDAS_all.npz" 
save_path_WLDAS_dust = "histograms/WLDAS_dust.npz" 

# Loop through all NetCDF files in the directory
if os.path.exists(save_path):
    print(f"Loading data from {save_path}")
    # Load the data from the npz file
    data_WLDAS_all = np.load(save_path, allow_pickle=True)
    data_WLDAS_all = {key: data_WLDAS_all[key] for key in data_WLDAS_all.files}  # Convert to dictionary
else:
    print(f"{save_path} does not exist. Processing NetCDF files...")
    
    # Initialize data_WLDAS_all dictionary to store variables
    data_WLDAS_all = {}
    
    # Loop through all NetCDF files in the directory
    for filename in sorted(os.listdir(data_dir)):  # Sorted to maintain time order if filenames are chronological
        if filename.endswith(".nc"):
            file_path = os.path.join(data_dir, filename)

            # Open the NetCDF file
            ds = xr.open_dataset(file_path)
            print(f"Opened {filename}")

            # Aggregate data for each variable
            for var in ds.data_vars:
                data = ds[var].values.flatten()  # Flatten in case of multidimensional data

                # Store or append data
                if var not in data_WLDAS_all:
                    data_WLDAS_all[var] = data
                else:
                    data_WLDAS_all[var] = np.concatenate((data_WLDAS_all[var], data))

            ds.close()  # Close dataset
            print(f"Collected variables from {filename}")

    # Save the data as an npz file to avoid re-processing in the future
    print(f"Saving data to {save_path_WLDAS_all}")
    np.savez(save_path_WLDAS_all, **data_WLDAS_all)


#--- Create distribution for near dust events
file_path = '~/Dust_Analysis/dust_dataset_final_20241226.txt'
dust_df = pd.read_csv(file_path, sep=r'\s+', skiprows=2, header=None)
dust_df.columns = [
    'Date (YYYYMMDD)','start time (UTC)','latitude','longitude','Jesse Check'
]
print(dust_df.head())

# Extract latitude and longitude of dust events
dust_latitudes = dust_df['latitude'].values
dust_longitudes = dust_df['longitude'].values

# Loop through each dust event and filter WLDAS data for nearby points (1x1 degree box)
for idx, (dust_lat, dust_lon) in enumerate(zip(dust_latitudes, dust_longitudes)):
    print(f"Processing dust event {idx + 1}: Lat = {dust_lat}, Lon = {dust_lon}")
    
    # Initialize a dictionary to store data for the 1x1 box around this dust event
    data_WLDAS_dust = {var: [] for var in data_WLDAS_all.keys()}

    # Loop through all NetCDF files in the WLDAS data
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".nc"):
            file_path = os.path.join(data_dir, filename)
            ds = xr.open_dataset(file_path)
            ds = ds.squeeze()
            
            # Create masks to filter data within the 1x1 degree box around the dust event
            #--- fixing typos in longitudes
            def fix_typos(s):
                s = re.sub(r'^(\d+\.\d+)-$', r'-\1', s)
                return s   

            dust_lon = fix_typos(str(dust_lon))
            dust_lat = fix_typos(str(dust_lat))
            
            try:
                lat_mask = (ds['lat'].values >= float(dust_lat)) & (ds['lat'].values < float(dust_lat) + 1)
                lon_mask = (ds['lon'].values >= float(dust_lon)) & (ds['lon'].values < float(dust_lon) + 1)
                lat_mask_2d, lon_mask_2d = np.meshgrid(lat_mask, lon_mask, indexing='ij')
                full_mask = lat_mask_2d & lon_mask_2d
                full_mask_da = xr.DataArray(full_mask, dims=["lat", "lon"], coords={"lat": ds["lat"], "lon": ds["lon"]})
            except ValueError as e:
                print(f"Error occured for Lat = {dust_lat}, Lon = {dust_lon}: {e}")
                continue
            

            
            for var in ds.data_vars:
                if var == 'time_bnds':
                    continue
                try:
                    var_data = ds[var].where(full_mask_da, drop=True).values.flatten()
                    if len(var_data) > 0:
                        data_WLDAS_dust[var].extend(var_data)
                
                except Exception as e:
                    print(f"Error occurred for variable {var}: {e}")
                    continue
            
            ds.close()
            
            # Save the data as an npz file to avoid re-processing in the future
            print(f"Saving data to {save_path_WLDAS_dust}")
            np.savez(save_path_WLDAS_dust, **data_WLDAS_dust)

