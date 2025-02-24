#--- Plotting SWD files

import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.colors as mcolors

def plot_SWD(latitude_north, latitude_south, longitude_west, longitude_east, directory, file, year, month_num, month_name, day, hour, days_in_month):

    #--- Opening SWD from file
    SWD = xr.open_dataarray(file)

    #--- Plotting the SWD
    projection=ccrs.PlateCarree(central_longitude=0)
    fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})

    # cmap = LinearSegmentedColormap.from_list('custom_cmap', ['grey', 'white', 'blue'])
    # norm = TwoSlopeNorm(vmin=-12, vcenter=0, vmax=3)
    # levels = np.linspace(-12, 3, 31)
    #--- Colormap
    cmap_neg = plt.cm.Greys  # Greyscale for negative values (reversed for darker negatives)
    cmap_pos = plt.cm.rainbow  # Rainbow for positive values
    colors = np.vstack((cmap_neg(np.linspace(0, 1, 128)), cmap_pos(np.linspace(0, 1, 128))))
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", colors)
    vmin, vcenter, vmax = -3, 0, 2
    norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)

    # Define levels
    levels = np.linspace(vmin, vmax, 31)


    c=ax.contourf(SWD.lon, SWD.lat, SWD, cmap=cmap, extend='both', norm=norm, levels=levels)
    clb = plt.colorbar(c, shrink=0.4, pad=0.02, ax=ax)
    clb.ax.tick_params(labelsize=15)
    clb.set_label('(K)', fontsize=15)
    ax.set_extent([longitude_west, longitude_east, latitude_south, latitude_north], crs=ccrs.PlateCarree())

    if directory == "monthly_average":
        ax.set_title("GOES BTD (12.3 μm - 10.3 μm) Positive Average \n("+year+"/"+month_num+"/"+day+" "+hour+" - "+year+"/"+month_num+"/"+days_in_month+" "+hour+")", fontsize=20, pad=10)
    if directory == "swd_files":
        ax.set_title("GOES BTD (12.3 μm - 10.3 μm)\n("+year+"/"+month_num+"/"+day+" "+hour+")", fontsize=20, pad=10)
    if directory == "swd_adjusted":
        ax.set_title("GOES BTD (12.3 μm - 10.3 μm)\n("+year+"/"+month_num+"/"+day+" "+hour+", adjusted)", fontsize=20, pad=10)

    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(feature.STATES, zorder=100, edgecolor='#000', facecolor='none', linewidth=0.5)

    if directory == "monthly_average":
        fig.savefig("monthly_average/"+year+"_"+month_name+"_"+hour+"_SWD_average", dpi=200, bbox_inches='tight')
    if directory == "swd_files":
        fig.savefig("swd_images/"+year+"_"+month_num+"_"+day+"_"+hour+"_SWD", dpi=200, bbox_inches='tight')
    if directory == "swd_adjusted":
        fig.savefig("swd_adjusted/"+year+"_"+month_num+"_"+day+"_"+hour+"_SWD_adjusted", dpi=200, bbox_inches='tight')
    
    plt.close()

    return