
import matplotlib.pyplot as plt
import numpy as np
import re

#--- Load in the .npz data
npz_path = "histograms/" 
data_WLDAS_all = np.load(npz_path+"WLDAS_all.npz")
data_WLDAS_dust = np.load(npz_path+"WLDAS_dust.npz")

#--- Get the variable labels
value_label_mapping = [
    {"label": "AvgSurfT_tavg = Surface temperature (K)", "value": "AvgSurfT_tavg"},
    {"label": "BareSoilT_tavg = Bare soil temperature (K)", "value": "BareSoilT_tavg"},
    {"label": "CanopInt_tavg = Total canopy water storage (kg m-2)", "value": "CanopInt_tavg"},
    {"label": "ECanop_tavg = Interception evaporation (kg m-2 s-1)", "value": "ECanop_tavg"},
    {"label": "ESoil_tavg = Bare soil evaporation (kg m-2 s-1)","value": "ESoil_tavg"},
    {"label": "Evap_tavg = Total evapotranspiration (kg m-2 s-1)","value": "Evap_tavg"},
    {"label": "GWS_tavg = Ground water storage (mm)","value": "GWS_tavg"},
    {"label": "LWdown_f_tavg = Surface downward longwave radiation (W m-2)","value": "LWdown_f_tavg"},
    {"label": "Lwnet_tavg = Net downward longwave radiation (W m-2)","value": "Lwnet_tavg"},
    {"label": "Psurf_f_tavg = Surface pressure (Pa)","value": "Psurf_f_tavg"},
    {"label": "Qair_f_tavg = Specific humidity (kg kg-1)", "value": "Qair_f_tavg"},
    {"label": "Qg_tavg = Soil heat flux (W m-2)","value": "Qg_tavg"},
    {"label": "Qh_tavg = Sensible heat flux (W m-2)", "value": "Qh_tavg"},
    {"label": "Qle_tavg = Latent heat flux (W m-2)","value": "Qle_tavg"},
    {"label": "Qs_tavg = Surface runoff (kg m-2 s-1)","value": "Qs_tavg"},
    {"label": "Qsb_tavg = Subsurface runoff (kg m-2 s-1)","value": "Qsb_tavg"},
    {"label": "Qsm_tavg = Snow melt (kg m-2 s-1)","value": "Qsm_tavg"},
    {"label": "Rainf_f_tavg = Rainfall flux (kg m-2 s-1)","value": "Rainf_f_tavg"},
    {"label": "Rainf_tavg = Rain precipitation rate (kg m-2 s-1)","value": "Rainf_tavg"},
    {"label": "SnowDepth_tavg = Snow depth (m)","value": "SnowDepth_tavg"},
    {"label": "Snowcover_tavg = Snow cover (-)","value": "Snowcover_tavg"},
    {"label": "Snowf_tavg = Snowfall rate (kg m-2 s-1)","value": "Snowf_tavg"},
    {"label": "SoilMoi00_10cm_tavg = Soil moisture content (0-10 cm underground) (m^3 m-3)","value": "SoilMoi00_10cm_tavg"},
    {"label": "SoilMoi10_40cm_tavg = Soil moisture content (10-40 cm underground) (m^3 m-3)","value": "SoilMoi10_40cm_tavg"},
    {"label": "SoilMoi100_200cm_tavg = Soil moisture content (100-200 cm underground) (m^3 m-3)",
    "value": "SoilMoi100_200cm_tavg"},
{
    "label": "SoilMoi40_100cm_tavg = Soil moisture content (40-100 cm underground) (m^3 m-3)",
    "value": "SoilMoi40_100cm_tavg"
},
{
    "label": "SoilTemp00_10cm_tavg = Soil temperature (0-10 cm underground) (K)",
    "value": "SoilTemp00_10cm_tavg"
},
{
    "label": "SoilTemp10_40cm_tavg = Soil temperature (10-40 cm underground) (K)",
    "value": "SoilTemp10_40cm_tavg"
},
{
    "label": "SoilTemp100_200cm_tavg = Soil temperature (100-200 cm underground) (K)",
    "value": "SoilTemp100_200cm_tavg"
},
{
    "label": "SoilTemp40_100cm_tavg = Soil temperature (40-100 cm underground) (K)",
    "value": "SoilTemp40_100cm_tavg"
},
{
    "label": "SubSnow_tavg = snow sublimation (kg m-2 s-1)",
    "value": "SubSnow_tavg"
},
{
    "label": "SWdown_f_tavg = Surface downward shortwave radiation (W m-2)",
    "value": "SWdown_f_tavg"
},
{
    "label": "SWE_tavg = Snow water equivalent (kg m-2)",
    "value": "SWE_tavg"
},
{
    "label": "Swnet_tavg = Net downward shortwave radiation (W m-2)",
    "value": "Swnet_tavg"
},
{
    "label": "Tair_f_tavg = Air temperature (K)",
    "value": "Tair_f_tavg"
},
{
    "label": "TVeg_tavg = Vegetation transpiration (kg m-2 s-1)",
    "value": "TVeg_tavg"
},
{
    "label": "TWS_tavg = Terrestrial water storage (mm)",
    "value": "TWS_tavg"
},
{
    "label": "VegT_tavg = Canopy temperature (K)",
    "value": "VegT_tavg"
},
{
    "label": "WaterTableD_tavg = water table depth (m)",
    "value": "WaterTableD_tavg"
},
{
    "label": "Wind_f_tavg = Wind speed (m s-1)",
    "value": "Wind_f_tavg"
},
{
    "label": "WT_tavg = Water in aquifer and saturated soil (mm)",
    "value": "WT_tavg"
}
            ]
# Convert list to a dictionary for fast lookup
label_dict = {item['value']: item['label'] for item in value_label_mapping}


#--- Plot histograms: the WLDAS histogram and the dust-specific histogram
for var in data_WLDAS_all.keys():
    if len(data_WLDAS_dust[var]) > 0:
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # Determine the common range for x-axis
        x_min, x_max = np.nanmin(data_WLDAS_all[var]), np.nanmax(data_WLDAS_all[var])

        # First histogram on primary y-axis
        ax1.hist(data_WLDAS_all[var], bins=50, range=[x_min, x_max], edgecolor="blue", color='blue', alpha=0.7, label="WLDAS Data")
        ax1.set_ylabel("Frequency (WLDAS Data)", color="black")
        ax1.tick_params(axis='y', labelcolor="black")
        #ax1.set_xlim(x_min, x_max)

        # Create a second y-axis
        ax2 = ax1.twinx()
        ax2.hist(data_WLDAS_dust[var], bins=50, range=[x_min, x_max], edgecolor="orange", color='orange', alpha=0.7, label="Dust Region")
        ax2.set_ylabel("Frequency (Dust Region)", color="orange")
        ax2.tick_params(axis='y', labelcolor="orange")
        #ax2.set_xlim(x_min, x_max)

        label = label_dict.get(var, "Unknown Label")
        fig.legend(loc="upper right")
        ax1.set_title(f"Histogram of {label}")
        ax1.grid(True)
        
        # Sanitize the variable name to avoid invalid characters in filenames
        clean_var_name = f"{var.replace(' ', '_')}"
        clean_var_name = re.sub(r'[^A-Za-z0-9_-]', '', clean_var_name)
        
        # Save the figure
        fig.savefig(f"histograms/{clean_var_name}.png", dpi=200, bbox_inches='tight')
        plt.close()