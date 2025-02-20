#--- Plotting SWD files

import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

#--- Select region for visualization
#------ US Southwest (zoomed out)
latitude_north = 44
latitude_south = 27.5
longitude_west = -128
longitude_east = -100

#--- Select file
directory = "swd_adjusted"  #--- "swd_files" or "monthly_average" or "swd_adjusted"
year = "2025"
month_num = "01"
month_name = "Jan"
day = "30"
hour = "02Z"
days_in_month = "31"

#--- Opening SWD from file
if directory == "monthly_average":
    SWD = xr.open_dataarray(directory+"/"+year+"_"+month_name+"_"+hour+".nc")
if directory == "swd_files":
    SWD = xr.open_dataarray(directory+"/satellite_btd_"+year+"_"+month_num+"_"+day+"_"+hour+".nc")
if directory == "swd_adjusted":
    SWD = xr.open_dataarray(directory+"/"+year+"_"+month_num+"_"+day+"_"+hour+".nc")

#--- Plotting the SWD
projection=ccrs.PlateCarree(central_longitude=0)
fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['grey', 'white', 'red'])
norm = TwoSlopeNorm(vmin=-12, vcenter=0, vmax=3)
levels = np.linspace(-12, 3, 31)
c=ax.contourf(SWD.lon, SWD.lat, SWD, cmap=cmap, extend='both', norm=norm, levels=levels)
clb = plt.colorbar(c, shrink=0.4, pad=0.02, ax=ax)
clb.ax.tick_params(labelsize=15)
clb.set_label('(K)', fontsize=15)
ax.set_extent([longitude_west, longitude_east, latitude_south, latitude_north], crs=ccrs.PlateCarree())

if directory == "monthly_average":
    ax.set_title("GOES BTD (12.3 μm - 10.3 μm) Positive Average \n("+year+"/"+month_num+"/01 "+hour+" - "+year+"/"+month_num+"/"+days_in_month+" "+hour+")", fontsize=20, pad=10)
if directory == "swd_files":
    ax.set_title("GOES BTD (12.3 μm - 10.3 μm)\n("+year+"/"+month_num+"/01 "+hour+")", fontsize=20, pad=10)
if directory == "swd_adjusted":
    ax.set_title("GOES BTD (12.3 μm - 10.3 μm)\n("+year+"/"+month_num+"/01 "+hour+", adjusted)", fontsize=20, pad=10)

ax.coastlines(resolution='50m', color='black', linewidth=1)
ax.add_feature(feature.STATES, zorder=100, edgecolor='#000', facecolor='none', linewidth=0.5)

if directory == "monthly_average":
    fig.savefig("monthly_average/"+year+"_"+month_name+"_"+hour+"_SWD_average", dpi=200, bbox_inches='tight')
if directory == "swd_files":
    fig.savefig("swd_images/"+year+"_"+month_num+"_"+day+"_"+hour+"_SWD", dpi=200, bbox_inches='tight')
if directory == "swd_adjusted":
    fig.savefig("swd_adjusted/"+year+"_"+month_num+"_"+day+"_"+hour+"_SWD_adjusted", dpi=200, bbox_inches='tight')
