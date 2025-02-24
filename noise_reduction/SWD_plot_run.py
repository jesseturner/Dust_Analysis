import SWD_plot
import glob
import os

#--- Select directory
directory = "monthly_average"  #--- "swd_files" or "monthly_average" or "swd_adjusted"

#--- Select region
#------ US Southwest (zoomed out)
latitude_north = 44
latitude_south = 27.5
longitude_west = -128
longitude_east = -100

#--- Select files
year = "2025"
month_num = "01"
month_name = "Jan"
day = "30"
days_in_month = "31"

#--- Loop through swd_adjusted files
if directory == "swd_adjusted": 
    
    file_pattern = os.path.join(directory, f"{year}_{month_num}_{day}_*.nc")
    file_list = glob.glob(file_pattern)

    for file in file_list:
        print(f"Processing file: {file}")

        #--- get the hour in 00Z format
        filename = os.path.basename(file)
        parts = filename.split("_")
        hour = parts[3].split(".")[0]

        SWD_plot.plot_SWD(latitude_north, latitude_south, longitude_west, longitude_east, directory, file, year, month_num, month_name, day, hour, days_in_month)

#--- Loop through monthly_average files
if directory == "monthly_average": 
    
    file_pattern = os.path.join(directory, f"{year}_{month_name}_*.nc")
    file_list = glob.glob(file_pattern)

    for file in file_list:
        print(f"Processing file: {file}")

        #--- get the hour in 00Z format
        filename = os.path.basename(file)
        parts = filename.split("_")
        hour = parts[2].split(".")[0]

        SWD_plot.plot_SWD(latitude_north, latitude_south, longitude_west, longitude_east, directory, file, year, month_num, month_name, day, hour, days_in_month)


#--- Loop through swd_files files
if directory == "swd_files": 
    
    file_pattern = os.path.join(directory, f"satellite_btd_{year}_{month_num}_{day}_*.nc")
    file_list = glob.glob(file_pattern)

    for file in file_list:
        print(f"Processing file: {file}")

        #--- get the hour in 00Z format
        filename = os.path.basename(file)
        parts = filename.split("_")
        hour = parts[5].split(".")[0]

        SWD_plot.plot_SWD(latitude_north, latitude_south, longitude_west, longitude_east, directory, file, year, month_num, month_name, day, hour, days_in_month)