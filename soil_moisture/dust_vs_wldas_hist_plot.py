
import matplotlib.pyplot as plt
import numpy as np
import re

#--- Load in the .npz data
npz_path = "histograms/" 
data_WLDAS_all = np.load(npz_path+"WLDAS_all.npz")
data_WLDAS_dust = np.load(npz_path+"WLDAS_dust.npz")

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

        fig.legend(loc="upper right")
        ax1.set_title(f"Histogram of {var}")
        ax1.grid(True)
        
        # Sanitize the variable name to avoid invalid characters in filenames
        clean_var_name = f"dust_case_{var.replace(' ', '_')}"
        clean_var_name = re.sub(r'[^A-Za-z0-9_-]', '', clean_var_name)
        
        # Save the figure
        fig.savefig(f"histograms/{clean_var_name}.png", dpi=200, bbox_inches='tight')
        plt.close()