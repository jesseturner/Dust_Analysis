# Dust climatology compared to WLDAS soil moisture
## Use soil_moisture environment

import pandas as pd
import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import re

#--- Create distribution for total WLDAS
data_dir = "WLDAS"
variable_data = {}
save_path = "histograms/variable_data.npz" 

# Loop through all NetCDF files in the directory
if os.path.exists(save_path):
    print(f"Loading data from {save_path}")
    # Load the data from the npz file
    variable_data = np.load(save_path, allow_pickle=True)
    variable_data = {key: variable_data[key] for key in variable_data.files}  # Convert to dictionary
else:
    print(f"{save_path} does not exist. Processing NetCDF files...")
    
    # Initialize variable_data dictionary to store variables
    variable_data = {}
    
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
                if var not in variable_data:
                    variable_data[var] = data
                else:
                    variable_data[var] = np.concatenate((variable_data[var], data))

            ds.close()  # Close dataset
            print(f"Collected variables from {filename}")

    # Save the data as an npz file to avoid re-processing in the future
    print(f"Saving data to {save_path}")
    np.savez(save_path, **variable_data)


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
    dust_variable_data = {var: [] for var in variable_data.keys()}

    # Loop through all NetCDF files in the WLDAS data
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".nc"):
            file_path = os.path.join(data_dir, filename)
            ds = xr.open_dataset(file_path)
            ds = ds.squeeze()
            
            # Create masks to filter data within the 1x1 degree box around the dust event
            #--- fixing typos in longitudes
            def fix_trailing_minus(s):
                s = re.sub(r'^(\d+\.\d+)-$', r'-\1', s)
                if '-' not in s:
                    s = '-' + s
                return s
            dust_lon = fix_trailing_minus(dust_lon)

            lat_mask = (ds['lat'].values >= float(dust_lat)) & (ds['lat'].values < float(dust_lat) + 1)
            lon_mask = (ds['lon'].values >= float(dust_lon)) & (ds['lon'].values < float(dust_lon) + 1)
            lat_mask_2d, lon_mask_2d = np.meshgrid(lat_mask, lon_mask, indexing='ij')
            full_mask = lat_mask_2d & lon_mask_2d

            
            for var in ds.data_vars:
                try:
                    var_data = ds[var].where(full_mask, drop=True).values.flatten()
                    if len(var_data) > 0:
                        dust_variable_data[var].extend(var_data)
                
                except Exception as e:
                    print(f"Error occurred for variable {var}: {e}")
                    continue
            
            ds.close()

#--- Plot histograms: the WLDAS histogram and the dust-specific histogram
for var in variable_data.keys():
    if len(dust_variable_data[var]) > 0:
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # First histogram on primary y-axis
        ax1.hist(variable_data[var], bins=50, edgecolor="black", alpha=0.7, label="WLDAS Data")
        ax1.set_ylabel("Frequency (WLDAS Data)", color="black")
        ax1.tick_params(axis='y', labelcolor="black")

        # Create a second y-axis
        ax2 = ax1.twinx()
        ax2.hist(dust_variable_data[var], bins=50, edgecolor="orange", alpha=0.7, label="Dust Region", color='orange')
        ax2.set_ylabel("Frequency (Dust Region)", color="orange")
        ax2.tick_params(axis='y', labelcolor="orange")

        fig.legend(loc="upper right")
        ax1.set_title(f"Histogram of {var}")
        ax1.grid(True)
        
        # Sanitize the variable name to avoid invalid characters in filenames
        clean_var_name = f"dust_case_{var.replace(' ', '_')}"
        clean_var_name = re.sub(r'[^A-Za-z0-9_-]', '', clean_var_name)
        
        # Save the figure
        fig.savefig(f"histograms/{clean_var_name}.png", dpi=200, bbox_inches='tight')
        plt.close()
