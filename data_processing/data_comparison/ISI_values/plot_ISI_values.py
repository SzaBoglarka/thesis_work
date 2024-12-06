import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors


# Load the JSON data
def load_from_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


# Function to normalize, plot ISI values, and fit a log line
def plot_isi_data_with_log_fit(cells_data, species, ax, x_length=None, color='blue',
                               label='', isi_type='steady_state', plot_only_one_mouse=False,
                               plot_all=True, cut_after_800ms=False):
    """
    Plot ISI values for a given species (RAT/MOUSE) on the subplot.
    Fit a logarithmic curve to each cell's ISI data.
    Only plot steady_state or highfreq_firing ISI values based on `isi_type`.
    """
    all_isi_lengths = []
    mouse_cells = []

    if species == 'RAT':
        color_path = './config/colors_RAT.json'
    else:
        color_path = './config/colors_MOUSE.json'
    # Load the colors from the JSON file
    with open(color_path, 'r') as f:
        colors = json.load(f)
    colors_ordered = []

    # Gather ISI values for the selected species and ISI type
    isi_data_list = []
    for cell_id, cell_info in cells_data.items():

        if cell_info['species'] == species:

            if plot_only_one_mouse:
                if species == 'MOUSE':
                    cell_id_short = cell_id[:10]
                    if cell_id_short not in mouse_cells:
                        mouse_cells.append(cell_id_short)
                    else:
                        continue

            if species == 'MOUSE':
                cell_id_color = cell_id[:10]
            else:
                cell_id_color = cell_id
            colors_ordered.append(colors[cell_id_color])

            if plot_all:
                if isi_type == 'steady_state':
                    isi_values = cell_info['isi_steady_state']  # Plot only steady_state ISI values
                    time_to_first_spike = cell_info['time_to_first_spike_steady']
                else:
                    isi_values = cell_info['isi_highfreq_firing']  # Plot only highfreq_firing ISI values
                    time_to_first_spike = cell_info['time_to_first_spike_highfreq']

            else:
                if cell_info['species'] == species:
                    if isi_type == 'steady_state':
                        isi_values = cell_info['isi_steady_state'][1:]  # Plot only steady_state ISI values
                        time_to_first_spike = cell_info['time_to_first_spike_steady']
                    else:
                        isi_values = cell_info['isi_highfreq_firing'][1:]  # Plot only highfreq_firing ISI values
                        time_to_first_spike = cell_info['time_to_first_spike_highfreq']

            if cut_after_800ms:
                isi_values_until_800ms = []
                if len(time_to_first_spike) != 0:
                    sum_isis = time_to_first_spike[0]
                else:
                    sum_isis = 0
                all_isis = len(isi_values)
                for i, isi in enumerate(isi_values):
                    sum_isis = sum_isis + isi
                    if sum_isis < 800:
                        isi_values_until_800ms.append(isi)
                    else:
                        print(f"Cut ISI_values at {i}/{all_isis}")
                        break
                isi_values = isi_values_until_800ms

            isi_data_list.append(isi_values)
            all_isi_lengths.append(len(isi_values))


    # Determine max length if not provided (for the x-axis normalization)
    if x_length is None:
        x_length = max(all_isi_lengths)

    # Normalize x-axis for each ISI list and plot
    for i, isi_values in enumerate(isi_data_list):
        n_points = len(isi_values)
        x_values = np.linspace(1, x_length, n_points)  # Start from 1 to avoid log(0)

        # Scatter plot the ISI values
        ax.plot(x_values, isi_values,
                color=colors_ordered[i],
                alpha=0.5,
                label=f'{species} {label}' if len(isi_data_list) == 1 else "",
                linestyle='',  # No line between points
                marker='o',  # Use circles as markers
                markerfacecolor='none'  # Hollow markers (no fill)
                )

        # It looks good, but we can't really use log func here - cannot justify it
        # Logarithmic fit: fit y = a * log(x) + b
        log_x = np.log(x_values)  # Take log of x-values
        coeffs = np.polyfit(log_x, isi_values, 1)  # Fit line to log(x) and y
        # Generate fitted values based on the log fit
        fitted_values = coeffs[0] * log_x + coeffs[1]
        # Plot the fitted log line
        #ax.plot(x_values, fitted_values, color=colors_ordered[i], linestyle='--', alpha=0.7)

        # Fit a straight line to the data
        coeffs = np.polyfit(x_values, isi_values, 1)  # Fit line to x and y
        # Generate fitted values based on the linear fit
        fitted_values = coeffs[0] * x_values + coeffs[1]  # y = mx + b
        ax.plot(x_values, fitted_values, color=colors_ordered[i], linestyle='--', alpha=0.7,
                label='Linear Fit')  # Plot the fitted line

    return x_length


# Path to the saved JSON file
json_file_path = "all_ISI_data.json"
# steady_state or highfreq_firing
current_type = 'highfreq_firing'
plot_all = False
save_fig = (f'./figures/'
            f'MOUSE_vs_RAT_ISI_values_{current_type}_until_800ms'
            f'_colorful_from_second_linear_fit_new.png')

currents = {
    'steady_state': {
        'name': 'Steady State',
        'ylim': 90,
        'ylim_plot_from_second': 90
    },
    'highfreq_firing': {
        'name': 'High-Frequency Firing',
        'ylim': 20,
        'ylim_plot_from_second': 10
    },
}

# Load data
data = load_from_json(json_file_path)

# Set global font size for readability
plt.rcParams.update({'font.size': 14, 'axes.labelsize': 16, 'axes.titlesize': 18, 'xtick.labelsize': 14, 'ytick.labelsize': 14})

# Create a figure with two subplots (one for MOUSE, one for RAT)
fig, (ax_mouse, ax_rat) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

# Plot MOUSE data on the top subplot
mouse_x_length = plot_isi_data_with_log_fit(data, "MOUSE", ax_mouse, color='green', label="MOUSE",
                                            isi_type=current_type, plot_only_one_mouse=True, plot_all=plot_all)
# Plot RAT data on the bottom subplot, using the same x_length as MOUSE
plot_isi_data_with_log_fit(data, "RAT", ax_rat, x_length=mouse_x_length, color='red', label="RAT",
                           isi_type=current_type, plot_all=plot_all, cut_after_800ms=True)

# Set x-axis labels for both plots: 'first' at 1 and 'last' at the end
ax_rat.set_xticks([1, mouse_x_length])
if plot_all:
    ax_rat.set_xticklabels(['first', 'last'])
else:
    ax_rat.set_xticklabels(['Second', 'Last'])

# Set y-axis label for both plots
ax_mouse.set_ylabel("ISI value (ms)")
ax_rat.set_ylabel("ISI value (ms)")

# Add titles for the subplots
ax_mouse.set_title(f"Mouse ISI Values during {currents[current_type]['name']}")
ax_rat.set_title(f"Rat ISI Values during {currents[current_type]['name']}")

# Set ylim
if plot_all:
    ax_mouse.set_ylim(0, currents[current_type]['ylim'])
    ax_rat.set_ylim(0, currents[current_type]['ylim'])
else:
    ax_mouse.set_ylim(2, currents[current_type]['ylim_plot_from_second'])
    ax_rat.set_ylim(2, currents[current_type]['ylim_plot_from_second'])


# Remove borders (spines) and add subtle grid lines
for ax in (ax_mouse, ax_rat):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)

# Adjust layout and save figure
plt.tight_layout(pad=2.0)
plt.savefig(save_fig, dpi=300)  # Higher dpi for publication quality

