import SWD
import SWD_average
import SWD_adjusted
import datetime
import numpy as np
import os

#--- Select region
#------ US Southwest (zoomed out)
latitude_north = 44
latitude_south = 27.5
longitude_west = -128
longitude_east = -100

#--- Loop through days and hours
year = 2025
month = 1

for hour in range(0, 24):
    hour_str = str(hour).zfill(2)+"Z"
    month_str = str(month).zfill(2)

    clim_path = f"monthly_average/2025_{month_str}_{hour_str}.nc"
    
    if os.path.exists(clim_path):
        print("Climatology exists, skipping build.")
    
    else:
        print("Building climatology.")
        
        for day in range(1, 32):
            julian_day = datetime.datetime(year, month, day).strftime('%j')
            datetime_str = str(year)+'-'+str(month).zfill(2)+'-'+str(day).zfill(2)+' '+str(hour).zfill(2)+'Z'

            #--- Checking if file has already been made
            date_str = str(datetime_str).replace('-', '_').replace(' ', '_')
            file_path = f"swd_files/satellite_btd_{date_str}.nc"
            if os.path.exists(file_path):
                print(f"{date_str} already exists.")
            else: 
                #--- Building the swd_file
                SWD.makeSWD(year, julian_day, month, day, hour, datetime_str, latitude_north, latitude_south, longitude_west, longitude_east)
        
        #--- Building the monthly_average
        median_data = SWD_average.make_average(hour_str, latitude_north, latitude_south, longitude_west, longitude_east)
    
    #--- Building the swd_adjusted
    adjusted_data = SWD_adjusted.make_adjusted(hour_str, latitude_north, latitude_south, longitude_west, longitude_east)
