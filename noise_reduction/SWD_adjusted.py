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

    #--- plot and save the adjusted SWD
    projection=ccrs.PlateCarree(central_longitude=0)
    fig,ax=plt.subplots(1, figsize=(12,12),subplot_kw={'projection': projection})
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
    cmap = LinearSegmentedColormap.from_list('custom_cmap', ['grey', 'white', 'red'])
    norm = TwoSlopeNorm(vmin=-12, vcenter=0, vmax=3)
    levels = np.linspace(-12, 3, 31)
    c=ax.contourf(SWD_adjusted.lon, SWD_adjusted.lat, SWD_adjusted, cmap=cmap, extend='both', norm=norm, levels=levels)
    clb = plt.colorbar(c, shrink=0.4, pad=0.02, ax=ax)
    clb.ax.tick_params(labelsize=15)
    clb.set_label('(K)', fontsize=15)
    ax.set_extent([longitude_west, longitude_east, latitude_south, latitude_north], crs=ccrs.PlateCarree())
    ax.set_title("GOES BTD (12.3 μm - 10.3 μm)\n(2025_01_30_"+utc+", adjusted)", fontsize=20, pad=10)
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(feature.STATES, zorder=100, edgecolor='#000', facecolor='none', linewidth=0.5)
    fig.savefig("swd_adjusted/2025_01_30_"+utc+"_SWD_adjusted", dpi=200, bbox_inches='tight')

    return SWD_adjusted