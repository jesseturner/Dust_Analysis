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
    
    # Ensure the dust latitudes and longitudes are float types
    dust_lat = float(dust_lat)
    dust_lon = float(dust_lon)
    
    # Initialize a dictionary to store data for the 1x1 box around this dust event
    dust_variable_data = {var: [] for var in variable_data.keys()}

    # Loop through all NetCDF files in the WLDAS data
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".nc"):
            file_path = os.path.join(data_dir, filename)
            ds = xr.open_dataset(file_path)
            
            # Ensure the latitude and longitude arrays in WLDAS are floats
            lat = ds['lat'].values.astype(float)  # Convert to float
            lon = ds['lon'].values.astype(float)  # Convert to float
            
            # Create masks to filter data within the 1x1 degree box around the dust event
            lat_mask = (lat >= dust_lat) & (lat < dust_lat + 1)
            lon_mask = (lon >= dust_lon) & (lon < dust_lon + 1)
            
#------ This line is where things get screwed up
            for var in variable_data.keys():
                try:
                    # Try to extract the data
                    var_data = ds[var].sel(lat=lat[lat_mask], lon=lon[lon_mask]).values.flatten()
                    
                    # Continue with your logic if there's no error
                    if len(var_data) > 0:
                        dust_variable_data[var].extend(var_data)
                
                except Exception as e:
                    # Log or print the error message
                    print(f"Error occurred for variable {var}: {e}")
                    # Skip the loop iteration and move to the next one
                    continue
            # Apply the masks to the variable data
            # for var in ds.data_vars:
            #     var_data = ds[var].sel(lat=lat[lat_mask], lon=lon[lon_mask]).values.flatten()
                
            #     # Store the filtered data in dust_variable_data for later histogram plotting
            #     if len(var_data) > 0:
            #         dust_variable_data[var].extend(var_data)
            
            ds.close()

    # Plot histograms: the WLDAS histogram and the dust-specific histogram
    for var in variable_data.keys():
        if len(dust_variable_data[var]) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(variable_data[var], bins=50, edgecolor="black", alpha=0.7, label="WLDAS Data")
            ax.hist(dust_variable_data[var], bins=50, edgecolor="orange", alpha=0.7, label="Dust Region", color='orange')
            ax.set_xlabel(var)
            ax.set_ylabel("Frequency")
            ax.set_title(f"Histogram of {var} with Dust Event at Lat: {dust_lat}, Lon: {dust_lon}")
            ax.grid(True)
            ax.legend(loc="upper right")
            
            # Sanitize the variable name to avoid invalid characters in filenames
            clean_var_name = f"dust_case_{var.replace(' ', '_')}"
            clean_var_name = re.sub(r'[^A-Za-z0-9_-]', '', clean_var_name)
            
            # Save the figure
            fig.savefig(f"histograms/{clean_var_name}.png", dpi=200, bbox_inches='tight')
            plt.close()
