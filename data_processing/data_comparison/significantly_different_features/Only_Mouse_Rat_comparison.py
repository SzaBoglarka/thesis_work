import json
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec


# Use the "seaborn" style for better visuals
#plt.style.use("seaborn")

# Set font sizes and line widths for publication-quality visuals
mpl.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'lines.linewidth': 2,
    'axes.linewidth': 1.5,
})


# Paths for the JSON files
mouse_features_path = ('/home/szabobogi/BluePyEfe_standard_features/BluePyEfe/FINAL_PV_PTI_data/'
                       'features_for_validation/standard_features_for_validation_MOUSE_FINAL.json')
rat_features_path = ('/home/szabobogi/BluePyEfe_standard_features/BluePyEfe/FINAL_PV_PTI_data/'
                     'PTI_PV_standard_features_RAT_expdata_FINAL/standard_features_RAT_ORIGINAL_STDS.json')
#model_features_dir = ('/home/szabobogi/hippounit_standard_features/validation_results_MOUSE/'
#                      'results/somaticfeat/')
model_features_dir = ('/home/szabobogi/hippounit_standard_features/validation_results_RAT/'
                      'results/somaticfeat/')

# Paths for final model names and colors
model_names_path = '/home/szabobogi/hippounit_standard_features/visualization/config/model_final_names.json'
model_colors_path = '/home/szabobogi/hippounit_standard_features/visualization/config/modelcolors_vibrant_final.json'

# Model categories
point_models = sorted(["Neymotin_2011", "Neymotin_2013", "Stacey(rb)_2009", "Stacey(vd)_2009",
                       "Vladimirov_2013", "Hu(rb)_2018", "Hummos_2014"])
stylized_models = sorted(["Cuts&Poir_2015", "Lee_2014", "Turi_2019", "Saudargiene_2015",
                          "Bezaire_2016"])
detailed_models = sorted(["Saraga_2006_6.3_cels", "Tzilivaki1_2019_0.1_dt", "Tzilivaki4_2019_0.1_dt",
                          "Ferr&Asco_2015", "Migliore_2018", "Tzilivaki3_2019_0.1_dt",
                          "Tzilivaki2_2019_0.1_dt", "Tzilivaki5_2019_0.1_dt", "Chiovini_2014"])

# Grouping features based on core feature name
grouped_features = {
    'AP_amplitude': ['AP_amplitude.steady_state_current', 'AP_amplitude.highfreq_firing_current'],
    #'AP_height': ['AP_height.rheobase_current', 'AP_height.steady_state_current', 'AP_height.highfreq_firing_current'],
    'AP_rise_rate': ['AP_rise_rate.steady_state_current', 'AP_rise_rate.highfreq_firing_current'],
    'ISI_log_slope': ['ISI_log_slope.steady_state_current', 'ISI_log_slope.highfreq_firing_current'],
    'fast_AHP_change': ['fast_AHP_change.steady_state_current', 'fast_AHP_change.highfreq_firing_current'],
    'Currents': ['rheobase_current.global', 'steady_state_current.global', 'highfreq_firing_current.global']
}

# Function to load JSON data from file
def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

# Load mouse and rat data
mouse_data = load_json(mouse_features_path)
rat_data = load_json(rat_features_path)

# Load model final names and colors
model_names = load_json(model_names_path)
model_colors = load_json(model_colors_path)

# Function to load the model data from file
def load_model_data(model_name):
    model_path = os.path.join(model_features_dir, model_name, 'somatic_model_features.json')
    with open(model_path, 'r') as f:
        return json.load(f)


# Function to plot only the experimental mouse and rat data with custom subplot widths
def plot_experimental_data_custom_width(save_path):
    # Create a figure with a 3x3 grid layout using GridSpec
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 3, figure=fig)

    # Define axes based on GridSpec, with custom widths for each subplot
    axes = [
        fig.add_subplot(gs[0, 0]),  # Narrow plot
        fig.add_subplot(gs[0, 1]),  # Narrow plot
        fig.add_subplot(gs[1, 0]),  # Narrow plot
        fig.add_subplot(gs[1, 1]),  # Narrow plot
        fig.add_subplot(gs[2, :2]),  # Wide plot spanning two columns
        fig.add_subplot(gs[0:2, 2])  # Empty spot for legend in the top right
    ]

    # Plot data for each group of features except `AP_height`
    for i, (core_feature, feature_list) in enumerate(grouped_features.items()):
        if i >= 5:  # We only have 5 features to plot
            break
        ax = axes[i]
        x_labels = []
        x_pos = []

        # Plot experimental mouse and rat data only
        for j, feature in enumerate(feature_list):
            mouse_mean = float(mouse_data.get(feature, {}).get('Mean', 0))
            mouse_std = float(mouse_data.get(feature, {}).get('Std', 0))
            rat_mean = float(rat_data.get(feature, {}).get('Mean', 0))
            rat_std = float(rat_data.get(feature, {}).get('Std', 0))

            x_base = j * 3
            x_labels.append(feature.split('.')[1] if '.' in feature else feature)
            x_pos.append(x_base + 0.5)

            # Plot mouse and rat data with error bars
            ax.errorbar([x_base], [mouse_mean], yerr=[mouse_std], fmt='x', color='b', label='Mouse' if j == 0 else "")
            ax.errorbar([x_base + 0.5], [rat_mean], yerr=[rat_std], fmt='x', color='g', label='Rat' if j == 0 else "")

        # Set title, labels, and ticks
        ax.set_title(core_feature, fontsize=16)
        ax.set_ylabel('Values')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels)

        # Remove borders and add grid lines for clarity
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Add a single legend for mouse and rat data in the empty subplot area
    handles, labels = axes[0].get_legend_handles_labels()
    axes[-1].axis('off')  # Turn off this axis for legend use only
    fig.legend(handles, labels, loc='center', frameon=False, ncol=1, bbox_to_anchor=(0.75, 0.5))

    '''
    # Set individual y-axis limits for each feature plot, as per original layout
    axes[0].set_ylim(20, 110)
    axes[1].set_ylim(0, 280)
    axes[2].set_ylim(-0.15, 0.22)
    axes[3].set_ylim(-0.25, 1.75)
    axes[4].set_ylim(-0.1, 1.05)
    '''

    # Save with high DPI for publication
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


# Call the function to generate the plot with custom subplot widths
plot_experimental_data_custom_width('Exp_data_only_custom_width_comparison.png')
print("Experimental data plot with custom widths saved successfully.")