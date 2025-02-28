
import matplotlib.pyplot as plt

#--- Load in the .npz data

#--- Plot histograms: the WLDAS histogram and the dust-specific histogram
for var in variable_data.keys():
    if len(data_WLDAS_dust[var]) > 0:
        fig, ax1 = plt.subplots(figsize=(10, 5))

        # First histogram on primary y-axis
        ax1.hist(variable_data[var], bins=50, edgecolor="black", alpha=0.7, label="WLDAS Data")
        ax1.set_ylabel("Frequency (WLDAS Data)", color="black")
        ax1.tick_params(axis='y', labelcolor="black")

        # Create a second y-axis
        ax2 = ax1.twinx()
        ax2.hist(data_WLDAS_dust[var], bins=50, edgecolor="orange", alpha=0.7, label="Dust Region", color='orange')
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