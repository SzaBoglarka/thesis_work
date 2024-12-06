import json
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

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


# Function to plot the model category with shifting and alpha, enhanced for publication
def plot_models_for_category(model_list, category_name, marker, marker_size, save_path):
    # Adjust layout to have 5 subplots in a grid of 3 rows x 2 columns (last row has one plot and a legend)
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    axes = axes.flatten()

    # Plot data for each group of features except `AP_height`
    for i, (core_feature, feature_list) in enumerate(grouped_features.items()):
        ax = axes[i]

        x_labels = []
        x_pos = []

        # Plot experimental mouse and rat data
        for j, feature in enumerate(feature_list):
            mouse_mean = float(mouse_data.get(feature, {}).get('Mean', 0))
            mouse_std = float(mouse_data.get(feature, {}).get('Std', 0))
            rat_mean = float(rat_data.get(feature, {}).get('Mean', 0))
            rat_std = float(rat_data.get(feature, {}).get('Std', 0))

            x_base = j * 3
            if feature.split('.')[1] == 'global':
                x_labels.append(feature.split('.')[0])  # Get stimulus type (e.g., steady_state_current)
            else:
                x_labels.append(feature.split('.')[1])  # Get stimulus type (e.g., steady_state_current)
            x_pos.append(x_base + 0.5)

            ax.errorbar([x_base], [mouse_mean], yerr=[mouse_std], fmt='x', label='Mouse' if j == 0 else "", color='b')
            ax.errorbar([x_base + 0.5], [rat_mean], yerr=[rat_std], fmt='x', label='Rat' if j == 0 else "", color='g')

        # Plot model data for this category with shifts and transparency
        shift_step = 0.05  # Shift for each model
        for k, model_name in enumerate(model_list):
            model_data = load_model_data(model_name)
            for j, feature in enumerate(feature_list):
                model_mean = float(model_data.get(feature, {}).get('feature mean', 0))
                x_base = j * 3

                final_name = model_names[model_name]
                color = model_colors[final_name]

                x_shifted = x_base + 1 + (k * shift_step)

                ax.scatter([x_shifted], [model_mean], label=final_name if j == 0 else "", color=color,
                           marker=marker, s=marker_size, alpha=0.7)

        # Set title, labels, and ticks
        ax.set_title(core_feature, fontsize=16)
        ax.set_ylabel('Values')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels )
        # Remove borders (spines) and add subtle grid lines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add grid for better readability
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    ## Move the legend to the last subplot (bottom-right) and adjust figure layout
    #axes[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Models", frameon=False)
    axes[-1].axis('off')  # Hide the last subplot (used only for legend)

    # Add the legend only on the last subplot (for layout consistency)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(0.9, 0.1), frameon=False, ncol=2)


    # Remove any unused subplots (after AP_height is removed)
    for ax in axes[i + 1:-1]:
        ax.axis('off')

    axes[0].set_ylim(20, 110)
    axes[1].set_ylim(0, 280)
    axes[2].set_ylim(-0.15, 0.22)
    axes[3].set_ylim(-0.25, 1.75)
    axes[4].set_ylim(-0.1, 1.05)


    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')  # Save with high DPI for publication
    plt.close()


# Plot and save figures for each model category with enhanced aesthetics
plot_models_for_category(point_models, 'Point Models',
                         'o', 110,
                         'Exp_data_VS_point_models_comparison.png')
plot_models_for_category(stylized_models, 'Stylized Models',
                         '^', 120,
                         'Exp_data_VS_stylized_models_comparison.png')
plot_models_for_category(detailed_models, 'Detailed Models',
                         '*', 180,
                         'Exp_data_VS_val_detailed_models_comparison.png')

print("Figures saved successfully with publication-quality formatting.")
