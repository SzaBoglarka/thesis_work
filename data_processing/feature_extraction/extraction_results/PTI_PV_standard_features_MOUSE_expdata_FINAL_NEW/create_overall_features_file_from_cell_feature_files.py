import os
import json
from venv import create

import numpy as np
from collections import defaultdict


# Step 1: Load all `features.json` files and group by cell ID
def load_features(folder_paths):
    print('starting the process')
    all_cell_data = []
    for cell_id in folder_paths:
        if len(cell_id)==10:
            file_path = os.path.join(cell_id, 'features.json')
            with open(file_path, 'r') as f:
                features = json.load(f)
            all_cell_data.append(features)
            print(cell_id)
    # print(cell_data)
    return all_cell_data


# Step 2: Calculate mean and std for each feature based on the cell data
def create_cell_features_files(all_cell_data):
    overall_means = {}
    for feature_group in all_cell_data[0].keys():  # Iterate over categories ('global', 'rheobase_current', etc.)
        if feature_group in ['global', 'standard_negative_current', 'rheobase_prev_current',
                             'rheobase_current', 'steady_state_current', 'highfreq_firing_current']:

            overall_means[feature_group] = {}
            overall_means[feature_group]['soma'] = []

            # Collect feature mean values for each cell
            all_cells_feature_mean_values = defaultdict(list)
            for cell_features in all_cell_data:
                for feature in cell_features[feature_group]['soma']:
                    # print(feature)
                    if 'current_val' not in feature.keys():
                        feature_name = feature['feature']
                        all_cells_feature_mean_values[feature_name].append(
                            feature['val'][0])  # Collect mean values for each feature
            # Calculate mean and std dev for each feature of the cell
            for feature_name, values in all_cells_feature_mean_values.items():
                # print('len(values)', len(values))
                cell_mean = np.mean(values)
                cell_std = np.std(values)
                overall_means[feature_group]['soma'].append(
                    {"feature": feature_name, "val": [cell_mean, cell_std], "n": len(values)})

    return overall_means


# Step 3: Save the overall means to `overall_mean_features.json`
def save_overall_mean_feature_values_file(overall_feat_file):
    output_path = 'corrected_features.json'
    with open(output_path, 'w') as outfile:
        json.dump(overall_feat_file, outfile, indent=2)
    print(f"Cell features.json file saved to {output_path}")


folder_paths = [
    "d180601_01",
    "d190218_01",
    "r180605_03",
    "r190218_02",
    "r190531_02",
    "r190531_04",
]

# Load feature data and process
all_cell_data = load_features(folder_paths)
overall_feat_means_file = create_cell_features_files(all_cell_data)
print(overall_feat_means_file)
save_overall_mean_feature_values_file(overall_feat_means_file)
