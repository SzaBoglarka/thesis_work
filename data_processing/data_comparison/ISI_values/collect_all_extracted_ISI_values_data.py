import os
import json


def load_feature_data(features_path):
    """Load the feature data from the features.json file for each cell and
    extract steady_state and highfreq_firing currents."""
    with open(features_path, 'r') as f:
        data = json.load(f)
    steady_state = None
    highfreq_firing = None
    if "global" in data and "soma" in data["global"]:
        for item in data["global"]["soma"]:
            if item["feature"] == "steady_state_current":
                steady_state = item["val"][0]
            elif item["feature"] == "highfreq_firing_current":
                highfreq_firing = item["val"][0]
    return steady_state, highfreq_firing


def load_isi_data(isi_file_path):
    """Load the all_ISI_values from the corresponding stim amplitude file."""
    with open(isi_file_path, 'r') as f:
        data = json.load(f)
    return data.get("all_ISI_values", [])


def load_time_to_first_spike_data(isi_file_path):
    """Load the all_ISI_values from the corresponding stim amplitude file."""
    with open(isi_file_path, 'r') as f:
        data = json.load(f)
    return data.get("time_to_first_spike", [])


def process_data(base_path):
    """Main function to process data from all folders and files."""
    # Define paths
    feat_paths = {
        "MOUSE": os.path.join(base_path, "feat_extr_MOUSE_expdata"),
        "RAT": os.path.join(base_path, "feat_extr_RAT_expdata")
    }
    stim_paths = {
        "MOUSE": os.path.join(base_path, "MOUSE"),
        "RAT": os.path.join(base_path, "RAT")
    }

    cell_data = {}
    # Iterate over both species folders (MOUSE and RAT)
    for species in ["MOUSE", "RAT"]:
        feat_dir = feat_paths[species]
        stim_dir = stim_paths[species]

        # Loop over each cell directory inside feat_extr_ folders
        for cell_id in os.listdir(feat_dir):
            cell_dir = os.path.join(feat_dir, cell_id)
            # Skip if it's not a directory
            if not os.path.isdir(cell_dir):
                continue
            features_path = os.path.join(cell_dir, "features.json")
            # Load features.json and extract currents
            steady_state_current, highfreq_firing_current = load_feature_data(features_path)
            # Only proceed if both values are found
            if steady_state_current is None or highfreq_firing_current is None:
                print(f'Could not read standard currents for cell {cell_id}')
                continue
            # Find the corresponding stim files for steady_state_current and highfreq_firing_current
            stim_file_steady = f"{cell_id}_{steady_state_current}.json"
            stim_file_highfreq = f"{cell_id}_{highfreq_firing_current}.json"
            # Load ISI data from corresponding stim files
            isi_steady_path = os.path.join(stim_dir, stim_file_steady)
            isi_highfreq_path = os.path.join(stim_dir, stim_file_highfreq)
            isi_steady_values = load_isi_data(isi_steady_path) \
                if os.path.exists(isi_steady_path) else []
            time_to_first_spike_steady = load_time_to_first_spike_data(isi_steady_path) \
                if os.path.exists(isi_steady_path) else []
            time_to_first_spike_highfreq = load_time_to_first_spike_data(isi_highfreq_path) \
                if os.path.exists(isi_highfreq_path) else []
            isi_highfreq_values = load_isi_data(isi_highfreq_path) \
                if os.path.exists(isi_highfreq_path) else []
            if not isi_steady_values or not isi_highfreq_values:
                print(f'Could not read ISI_values for cell {cell_id}')
            # Store the data in a structured dictionary
            cell_data[cell_id] = {
                "species": species,
                "steady_state_current": steady_state_current,
                "highfreq_firing_current": highfreq_firing_current,
                "isi_steady_state": isi_steady_values,
                "isi_highfreq_firing": isi_highfreq_values,
                "time_to_first_spike_steady": time_to_first_spike_steady,
                "time_to_first_spike_highfreq": time_to_first_spike_highfreq
            }

    return cell_data


def save_to_json(data, output_path):
    """Save the collected cell data into a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


# Base directory where the folders exist
base_path = "./"  # Replace with your actual base path
ISIs_data = process_data(base_path)
save_to_json(ISIs_data, './all_ISI_data.json')


# Print first few entries of the cell data
for cell_id, cell_info in list(ISIs_data.items())[:5]:
    print(f"Cell ID: {cell_id}")
    print(f"Species: {cell_info['species']}")
    print(f"Steady State Current: {cell_info['steady_state_current']}")
    print(f"Highfreq Firing Current: {cell_info['highfreq_firing_current']}")
    print(f"ISI (Steady State): {cell_info['isi_steady_state']}")
    print(f"ISI (Highfreq Firing): {cell_info['isi_highfreq_firing']}")
    print(f"time_to_first_spike_steady: {cell_info['time_to_first_spike_steady']}")
    print(f"time_to_first_spike_highfreq: {cell_info['time_to_first_spike_highfreq']}")
    print("\n")
