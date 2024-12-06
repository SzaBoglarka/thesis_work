import os
import json
import matplotlib.pyplot as plt
import numpy as np


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")


def find_item_with_feature(mouse_features_data, feature_name, standard_curr_name):
    mouse_feature_item = None
    for key, value in mouse_features_data.items():
        if key == standard_curr_name:
            for mouse_item in value["soma"]:
                if "feature" in mouse_item:
                    if mouse_item["feature"] == feature_name:
                        mouse_feature_item = mouse_item
                        break
    return mouse_feature_item


def replace_rat_stds_with_mouse_stds(mouse_features_data, rat_features_data):
    standard_curr_names = ['rheobase_current', 'rheobase_prev_current', 'steady_state_current',
                           'highfreq_firing_current', 'standard_negative_current', 'global']

    all_features = 0
    replaced_std = 0
    for key, value in rat_features_data.items():
        if key in standard_curr_names:
            for rat_item in value["soma"]:

                all_features += 1

                if "feature" in rat_item:
                    mouse_feature_item = (
                            find_item_with_feature(mouse_features_data, rat_item["feature"], key))
                    if mouse_feature_item:
                        rat_item["val"][1] = mouse_feature_item["val"][1]
                        replaced_std += 1
                    else:
                        print(f"No {key} {rat_item['feature']} in the mouse feature.json")

                if "current_val" in rat_item:
                    print('Skipping feature with current_value')
                    '''
                    rat_item["current_val"][1] \
                        = mouse_features_data[key]["soma"][0]["current_val"][1]
                    replaced_std += 1
                    '''
                    continue

                if "current_val_baseline_corrected" in rat_item:
                    rat_item["current_val_baseline_corrected"][1] \
                        = mouse_features_data[key]["soma"][1]["current_val_baseline_corrected"][1]
                    replaced_std += 1

    print(f"Replaced std in {replaced_std} of {all_features} items")

    return rat_features_data


path_mouse_features = './PTI_PV_standard_features_MOUSE_expdata_FINAL_NEW/corrected_features.json'
path_rat_features = './PTI_PV_standard_features_RAT_expdata_FINAL/features.json'

feature_data_mouse = load_json(path_mouse_features)
feature_data_rat = load_json(path_rat_features)

new_rat_features = replace_rat_stds_with_mouse_stds(feature_data_mouse, feature_data_rat)

# Save the dictionary to a JSON file with indentation
with open("./PTI_PV_standard_features_RAT_expdata_with_mouse_stds_FINAL/"
          "features.json", "w") as json_file:
    json.dump(new_rat_features, json_file, indent=4)

