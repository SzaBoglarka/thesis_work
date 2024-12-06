import os
import json
from venv import create

import numpy as np
from collections import defaultdict


# Step 1: Load all `features.json` files and group by cell ID
def load_features(folder_paths):
    print('starting the process')
    cell_data = defaultdict(list)
    for folder in folder_paths:
        if len(folder)>10:
            cell_id = folder[:10]  # Extract the first 10 characters as cell ID
            file_path = os.path.join(folder, 'features.json')
            with open(file_path, 'r') as f:
                features = json.load(f)
            cell_data[cell_id].append(features)
            print(cell_id)
    # print(cell_data)
    return cell_data


# Step 2: Calculate mean and std for each feature in each cell
def create_cell_features_files(cell_data):
    cell_means = {}
    for cell_id, feature_list in cell_data.items():
        cell_means[cell_id] = {}
        for feature_group in feature_list[0].keys():  # Iterate over categories ('global', 'rheobase_current', etc.)
            if feature_group in [ 'global', 'standard_negative_current', 'rheobase_prev_current',
                                  'rheobase_current', 'steady_state_current', 'highfreq_firing_current']:

                cell_means[cell_id][feature_group] = {}
                cell_means[cell_id][feature_group]['soma'] = []

                # Collect all feature values across different folders of the same cell
                feature_values = defaultdict(list)
                for features in feature_list:
                    for feature in features[feature_group]['soma']:
                        # print(feature)
                        if 'current_val' not in feature.keys():
                            feature_name = feature['feature']
                            feature_values[feature_name].append(feature['val'][0])  # Collect mean values for each feature
                # Calculate mean and std dev for each feature of the cell
                for feature_name, values in feature_values.items():
                    # print('len(values)', len(values))
                    cell_mean = np.mean(values)
                    cell_std = np.std(values)
                     #cell_means[cell_id][feature_group][feature_name] = {"val": [cell_mean, cell_std], "n": len(values)}
                    cell_means[cell_id][feature_group]['soma'].append({"feature": feature_name, "val": [cell_mean, cell_std], "n": len(values)})

    return cell_means


# Step 3: Save the overall means to `overall_mean_features.json`
def save_cell_feature_files(cell_feat_files):
    for cell in cell_feat_files.keys():
        cell_feat_file = cell_feat_files[cell]
        output_dir = os.path.join('./', cell)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'features.json')
        with open(output_path, 'w') as outfile:
            json.dump(cell_feat_file, outfile, indent=2)
        print(f"Cell features.json file saved to {output_path}")


folder_paths = [
    "d190218_0102", "d190218_0103", "d190218_0104", "d190218_0105",
    "r190531_0202", "r190531_0203", "r190531_0204", "r190531_0205",
    "r190531_0401", "r190531_0402", "r190531_0403", "r190531_0404"
]

# Load feature data and process
cell_data = load_features(folder_paths)
cell_feat_files = create_cell_features_files(cell_data)
print(cell_feat_files)
save_cell_feature_files(cell_feat_files)
#save_overall_means(overall_means)
