try:
    import cPickle as pickle
except:
    import pickle
import os
import numpy
import collections
import json
import scipy.stats as stats
import pandas as pd


# Create an empty DataFrame to store the results
columns = ['Feature Name', 'Mouse Mean', 'Mouse Std', 'Rat Mean', 'Rat Std',
           't-statistic', 'p-value', 'Significant', 'Corrected p-value', 'Significant after correction']
results_df = pd.DataFrame(columns=columns)

#base_dir = '/home/szabobogi/hippounit_standard_features/hippounit/validation_results/results/somaticfeat/'
save_dir = './'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Loading observation: MOUSE data
with open('/home/szabobogi/BluePyEfe_standard_features/BluePyEfe/FINAL_PV_PTI_data/'
          'features_for_validation/standard_features_for_validation_MOUSE_FINAL_NEW.json') as f:
    observation_MOUSE = json.load(f, object_pairs_hook=collections.OrderedDict)

# Loading observation: RAT data
with open('/home/szabobogi/BluePyEfe_standard_features/BluePyEfe/FINAL_PV_PTI_data/'
          'PTI_PV_standard_features_RAT_expdata_FINAL/standard_features_RAT_ORIGINAL_STDS.json') as f:
    observation_RAT = json.load(f, object_pairs_hook=collections.OrderedDict)


# Loading feature selection dictionary
with open('../features_for_validation/feature_selection.json') as f:
    all_features_dict = json.load(f, object_pairs_hook=collections.OrderedDict)


experimental_data = [observation_MOUSE, observation_RAT]
experiment_labels = ["mouse", "rat"]

n_MOUSE = 6  # Sample size for mouse data
n_RAT = 5
n_allfeatures = 181

sign_diff_feats = []
sign_diff_p_values = []

all_features_list = (all_features_dict['all_features']['first_problematic']
                     + all_features_dict['all_features']['only_negative']
                     + all_features_dict['all_features']['only_positive']
                     + all_features_dict['all_features']['negative_and_positive']
                     + all_features_dict['all_features']['global']
                     + all_features_dict['all_features']['rheobase']
                     + all_features_dict['all_features']['rheobase_prev'])

# those features that can be affected by the different time duration of the stim should be excluded here
# also those features, that measure the last AP could be excluded as well e.g. amp_drop_first_last
# could be excluded: steady_state_voltage_stimend, AP_amplitude_change, fast_AHP_change, AP_duration_change, AP_rise_rate_change
features_to_exclude_from_comparison = ['Spikecount', 'Spikecount_stimint', 'time_to_last_spike', 'mean_frequency',
                                       'steady_state_voltage_stimend']

all_features_list = sorted(all_features_list)

print(f"Significantly different features:\n")
count = 0
count_all = 0

for i in range(len(list(observation_MOUSE.keys()))):

    feature_name = list(observation_MOUSE.keys())[i]
    feature_name_short = feature_name.split('.')[0]

    if feature_name_short not in features_to_exclude_from_comparison:

        feat_mean_MOUSE = float(observation_MOUSE[feature_name]['Mean'])
        feat_std_MOUSE = float(observation_MOUSE[feature_name]['Std'])
        feat_mean_RAT = float(observation_RAT[feature_name]['Mean'])
        feat_std_RAT = float(observation_RAT[feature_name]['Std'])

        t_stat, p_value = stats.ttest_ind_from_stats(mean1=feat_mean_MOUSE, std1=feat_std_MOUSE, nobs1=n_MOUSE,
                                                     mean2=feat_mean_RAT, std2=feat_std_RAT, nobs2=n_RAT, equal_var=False)

        count_all += 1
        # print(f"Feature {feature_name}: t-statistic = {t_stat:.4f}, p-value = {p_value:.4e}")

        if p_value < 0.05:
            corrected_p_value = min(p_value * n_allfeatures, 1.0)
            is_significant = corrected_p_value < 0.05

            # Append the results to the DataFrame using loc
            results_df.loc[len(results_df)] = [
                feature_name,
                round(feat_mean_MOUSE, 4),
                round(feat_std_MOUSE, 4),
                round(feat_mean_RAT, 4),
                round(feat_std_RAT, 4),
                round(t_stat, 4),
                round(p_value, 4),
                'yes',
                round(corrected_p_value, 4),
                is_significant
            ]

            if is_significant:
                print(f"Feature {feature_name}: t-statistic = {t_stat:.4f}, p-value = {p_value:.4e}")
                count += 1

print(f"\nFound significant difference in {count}/{count_all} features after the correction")

# Save the results to a CSV file for future use
results_df.to_csv(os.path.join(save_dir, 'significant_features.csv'), index=False)


