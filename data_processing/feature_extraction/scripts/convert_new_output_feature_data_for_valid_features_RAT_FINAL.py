import json
import collections


# Load data
with open('../PTI_PV_standard_features_RAT_expdata_with_mouse_stds_FINAL/features.json') as f:
    data = json.load(f, object_pairs_hook=collections.OrderedDict)

# Load feature selection
with open('./feature_selection.json') as f:
    feature_selection = json.load(f, object_pairs_hook=collections.OrderedDict)

#print data
valid_data = collections.OrderedDict()
stim_list = []
all_features = []
count_all_features = 0

for key, stim_dict in data.items():

    # Convert standard current features
    if 'step' not in key:
        for i in range(len(data[key]["soma"])):

            if list(data[key]["soma"][i].keys())[0] == 'feature':
                feat = data[key]["soma"][i]['feature']
                value = data[key]["soma"][i]['val']

                if (key == 'standard_negative_current' and
                        (feat in feature_selection["all_features"]["only_negative"] or
                         feat in feature_selection["all_features"]["negative_and_positive"])):
                    valid_data[feat + "." + key] = collections.OrderedDict(
                        {"Std": str(value[1]), "Mean": str(value[0]),
                         "Weight": "1", "Stimulus": key, "Type": feat})
                    all_features.append(feat + "." + key)
                    count_all_features += 1

                if (key == 'rheobase_prev_current' and
                        (feat in feature_selection["all_features"]["rheobase_prev"])):
                    valid_data[feat + "." + key] = collections.OrderedDict(
                        {"Std": str(value[1]), "Mean": str(value[0]),
                         "Weight": "1", "Stimulus": key, "Type": feat})
                    all_features.append(feat + "." + key)
                    count_all_features += 1

                if (key == 'rheobase_current' and
                        (feat in feature_selection["all_features"]["rheobase"])):
                    valid_data[feat + "." + key] = collections.OrderedDict(
                        {"Std": str(value[1]), "Mean": str(value[0]),
                         "Weight": "1", "Stimulus": key, "Type": feat})
                    all_features.append(feat + "." + key)
                    count_all_features += 1

                if ((key == 'steady_state_current' or key == 'highfreq_firing_current') and
                        (feat in feature_selection["all_features"]["first_problematic"] or
                         feat in feature_selection["all_features"]["only_positive"] or
                         feat in feature_selection["all_features"]["negative_and_positive"] or
                         key == "global")):
                    valid_data[feat + "." + key] = collections.OrderedDict(
                        {"Std": str(value[1]), "Mean": str(value[0]),
                         "Weight": "1", "Stimulus": key, "Type": feat})
                    all_features.append(feat + "." + key)
                    count_all_features += 1

                if (key == 'global' and
                        (feat in feature_selection["all_features"]["global"])):
                    valid_data[feat + "." + key] = collections.OrderedDict(
                        {"Std": str(value[1]), "Mean": str(value[0]),
                         "Weight": "1", "Stimulus": key, "Type": feat})
                    all_features.append(feat + "." + key)
                    count_all_features += 1


ordered_valid_data = collections.OrderedDict(sorted(valid_data.items()))

final_stim_amps = ['-0.10', '-0.02', '0.02', '0.04', '0.06', '0.08', '0.10',
                  '0.15', '0.20', '0.25', '0.30', '0.35', '0.40',
                  '0.50', '0.60', '0.70', '0.80', '0.90']

stim_data = {"stimuli": collections.OrderedDict()}
for i in range(len(final_stim_amps)):
    stim_data["stimuli"].update(
        {"Step" + str(final_stim_amps[i]):
             {"Delay": "200",
              "RecLocationX": "0.5",
              "TTX": "0.0",
              "StimLocationX": "0.5",
              "Threshold": "-10.0",
              "Amplitude": str(final_stim_amps[i]),
              "Duration": "1000.0",
              "HypAmp": "0.0",
              "Type": "SquarePulse",
              "StimSectionName": "soma[0]",
              "RecSectionName": "soma[0]"}
         }
    )


file_name_valid_data= 'standard_features_for_validation_RAT_FINAL.json'
json.dump(ordered_valid_data, open(file_name_valid_data, "w"), indent=4)

file_name_stim_data= '../stim_for_validation/stim_for_validation_RAT_FINAL.json'
json.dump(stim_data, open(file_name_stim_data, "w"), indent=4)

file_name_all_features= 'all_RAT_features.txt'
with open(file_name_all_features, 'w') as f:
    f.writelines("Number of final features:" + str(count_all_features) + '\n')
    for i in all_features:
        f.writelines(str(i) + '\n')

print("Number of final features:", count_all_features)
