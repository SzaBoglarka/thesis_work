import sys

try:
    import cPickle as pickle
except:
    import pickle

import logging
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

dt = 1./int(5000) * 1e3
dt_new2 = 1./int(20000) * 1e3
dt_new = 1./int(10000) * 1e3


config = {
    'features': {
        'step':["AHP1_depth_from_peak",
    "AHP2_depth_from_peak",
    "AHP_depth",
    "AHP_depth_abs",
    "AHP_depth_abs_slow",
    "AHP_depth_diff",
    "AHP_depth_from_peak",
    "AHP_slow_time",
    "AHP_time_from_peak",
    "AP1_amp",
    "AP1_begin_voltage",
    "AP1_begin_width",
    "AP1_peak",
    "AP1_width",
    "AP2_AP1_begin_width_diff",
    "AP2_AP1_diff",
    "AP2_AP1_peak_diff",
    "AP2_amp",
    "AP2_begin_voltage",
    "AP2_begin_width",
    "AP2_peak",
    "AP2_width",
    "AP_amplitude",
    "AP_amplitude_change",
    "AP_amplitude_diff",
    "AP_amplitude_from_voltagebase",
    "AP_begin_indices",
    "AP_begin_time",
    "AP_begin_voltage",
    "AP_begin_width",
    "AP_duration",
    "AP_duration_change",
    "AP_duration_half_width",
    "AP_duration_half_width_change",
    "AP_end_indices",
    "AP_fall_indices",
    "AP_fall_rate",
    "AP_fall_rate_change",
    "AP_fall_time",
    "AP_height",
    "AP_phaseslope",
#    "AP_phaseslope_AIS",       # unknown for the new efel version
    "AP_rise_indices",
    "AP_rise_rate",
    "AP_rise_rate_change",
    "AP_rise_time",
    "AP_width",
    "APlast_amp",
 #   "APlast_width", causes segmentation fault
#    "BAC_maximum_voltage",     # unknown for the new efel version
#    "BAC_width",               # unknown for the new efel version
#    "BPAPAmplitudeLoc1",       # unknown for the new efel version
#    "BPAPAmplitudeLoc2",       # unknown for the new efel version
#    "BPAPHeightLoc1",          # unknown for the new efel version
#    "BPAPHeightLoc2",          # unknown for the new efel version
#    "BPAPatt2",                # unknown for the new efel version
#    "BPAPatt3",                # unknown for the new efel version
    "ISI_CV",
    "ISI_log_slope",
    "ISI_log_slope_skip",
    "ISI_semilog_slope",
    "ISI_values",
    "Spikecount",
    "Spikecount_stimint",
    "adaptation_index",
    "adaptation_index2",
    "all_ISI_values",
    "amp_drop_first_last",
    "amp_drop_first_second",
    "amp_drop_second_last",
    "burst_ISI_indices",
    "burst_mean_freq",
    "burst_number",
#    "check_AISInitiation",     # unknown for the new efel version
    "decay_time_constant_after_stim",
    #"depolarized_base", causes segmentation fault
    "doublet_ISI",
    "fast_AHP",
    "fast_AHP_change",
    "interburst_voltage",
    "inv_fifth_ISI",
    "inv_first_ISI",
    "inv_fourth_ISI",
    "inv_last_ISI",
    "inv_second_ISI",
    "inv_third_ISI",
    "inv_time_to_first_spike",
    "irregularity_index",
    "is_not_stuck",
    "max_amp_difference",
    "maximum_voltage",
    "maximum_voltage_from_voltagebase",
    "mean_AP_amplitude",
    "mean_frequency",
#    "min_AHP_indices", causes segmentation fault
    "min_AHP_values",
    "min_voltage_between_spikes",
    "minimum_voltage",
    "number_initial_spikes",
    "ohmic_input_resistance",
    "ohmic_input_resistance_vb_ssse",
    "peak_indices",
#    "peak_time", already added in extractor.py
    "peak_voltage",
    "sag_amplitude",
    "sag_ratio1",
    "sag_ratio2",
    "single_burst_ratio",
    "spike_half_width",
    "spike_width2",
    "steady_state_hyper",
    "steady_state_voltage",
    "steady_state_voltage_stimend",
    "time",
    "time_constant",
    "time_to_first_spike",
    "time_to_last_spike",
    "time_to_second_spike",
    "trace_check",
    "voltage_after_stim",
    "voltage_base",
    "voltage_deflection",
    "voltage_deflection_begin",
    "voltage_deflection_vb_ssse",
    "voltage",
    "ISIs",
    "initburst_sahp",
    "initburst_sahp_vb",
    "initburst_sahp_ssse"
    ]
    },
    'path': '/home/szabobogi/Documents/KOKI_mouse_hippocampus_data/KOKI_format_FINAL/',
    'format': 'csv_lccr',
    # 'comment':  [],


    'cells': {

	'd180601_01':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['d180601_0102/d180601_0102_ch1_cols'], 'baseline_currents': [-0.150], 'wrong_traces': [[]], 'dt':dt_new, 'startstop':[200,1000], 'amplitudes': [0.010, -0.010, 0.020, -0.020, 0.030, -0.030, 0.040, -0.040, 0.050, -0.050, 0.060, -0.060, 0.070, -0.070, 0.080, -0.080, 0.090, -0.090, 0.100, -0.100, 0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.600], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

	'd190218_0102':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['d190218_0102/d190218_0102_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.015, -0.015, 0.030, -0.030, 0.045, -0.045, 0.060, -0.060, 0.075, -0.075, 0.090, -0.090, 0.105, -0.105, 0.120, -0.120, 0.135, -0.135, 0.150, -0.150, 0.225, 0.300, 0.375, 0.450, 0.600, 0.750, 0.900], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'd190218_0103':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['d190218_0103/d190218_0103_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.020, -0.020, 0.040, -0.040, 0.060, -0.060, 0.080, -0.080, 0.100, -0.100, 0.120, -0.120, 0.140, -0.140, 0.160, -0.160, 0.180, -0.180, 0.200, -0.200, 0.300, 0.400, 0.500, 0.600, 0.800, 1.000, 1.200], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'd190218_0104':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['d190218_0104/d190218_0104_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.020, -0.020, 0.040, -0.040, 0.060, -0.060, 0.080, -0.080, 0.100, -0.100, 0.120, -0.120, 0.140, -0.140, 0.160, -0.160, 0.180, -0.180, 0.200, -0.200, 0.300, 0.400, 0.500, 0.600, 0.800, 1.000, 1.200], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'd190218_0105':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['d190218_0105/d190218_0105_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.030, -0.030, 0.060, -0.060, 0.090, -0.090, 0.120, -0.120, 0.150, -0.150, 0.180, -0.180, 0.210, -0.210, 0.240, -0.240, 0.270, -0.270, 0.300, -0.300, 0.450, 0.600, 0.750, 0.900, 1.200, 1.500, 1.800], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r180605_03':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r180605_0301/r180605_0301_ch1_cols', 'r180605_0302/r180605_0302_ch1_cols', 'r180605_0304/r180605_0304_ch1_cols'], 'baseline_currents': [-0.070, -0.070, -0.070], 'wrong_traces': [[],[], []], 'dt':dt_new, 'startstop':[200,1000], 'amplitudes': [0.007, -0.007, 0.014, -0.014, 0.021, -0.021, 0.028, -0.028, 0.035, -0.035, 0.042, -0.042, 0.049, -0.049, 0.056, -0.056, 0.063, -0.063, 0.070, -0.070, 0.105, 0.140, 0.175, 0.210, 0.280, 0.350, 0.420], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190218_02':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190218_0201/r190218_0201_ch01_cols', 'r190218_0202/r190218_0202_ch01_cols', 'r190218_0203/r190218_0203_ch01_cols', 'r190218_0204/r190218_0204_ch01_cols', 'r190218_0205/r190218_0205_ch01_cols', 'r190218_0206/r190218_0206_ch01_cols'], 'baseline_currents': [-0.110, -0.110, -0.110, -0.100, -0.100, -0.100], 'wrong_traces': [[],[], [], [], [], []], 'dt':dt_new, 'startstop':[200,1000], 'amplitudes': [0.007, -0.007, 0.014, -0.014, 0.021, -0.021, 0.028, -0.028, 0.035, -0.035, 0.042, -0.042, 0.049, -0.049, 0.056, -0.056, 0.063, -0.063, 0.070, -0.070, 0.105, 0.140, 0.175, 0.210, 0.280, 0.350, 0.420], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0202':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0202/r190531_0202_ch01_cols'], 'baseline_currents': [-0.250], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.011, -0.011, 0.022, -0.022, 0.033, -0.033, 0.044, -0.044, 0.055, -0.055, 0.066, -0.066, 0.077, -0.077, 0.088, -0.088, 0.099, -0.099, 0.110, -0.110, 0.165, 0.220, 0.275, 0.330, 0.440, 0.550, 0.660], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

	'r190531_0203':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0203/r190531_0203_ch01_cols'], 'baseline_currents': [-0.250], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0204':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0204/r190531_0204_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0205':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0205/r190531_0205_ch01_cols'], 'baseline_currents': [-0.200], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0401':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0401/r190531_0401_ch01_cols'], 'baseline_currents': [-0.050], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0402':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0402/r190531_0402_ch01_cols'], 'baseline_currents': [-0.150], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0403':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0403/r190531_0403_ch01_cols'], 'baseline_currents': [-0.150], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.018, -0.018, 0.036, -0.036, 0.054, -0.054, 0.072, -0.072, 0.090, -0.090, 0.108, -0.108, 0.126, -0.126, 0.144, -0.144, 0.162, -0.162, 0.180, -0.180, 0.270, 0.360, 0.450, 0.540, 0.720, 0.900, 1.080], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    'r190531_0404':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['r190531_0404/r190531_0404_ch01_cols'], 'baseline_currents': [-0.150], 'wrong_traces': [[]], 'dt':dt_new2, 'startstop':[200,1000], 'amplitudes': [0.018, -0.018, 0.036, -0.036, 0.054, -0.054, 0.072, -0.072, 0.090, -0.090, 0.108, -0.108, 0.126, -0.126, 0.144, -0.144, 0.162, -0.162, 0.180, -0.180, 0.270, 0.360, 0.450, 0.540, 0.720, 0.900, 1.080], 'hypamp': 0.0,'ton':200, 'toff':1000}}},

    },


    'options': {
        'relative': False,  # is the target given relative or in absolute current?

        'tolerance': 0.0001,  # group features based on target +/- this tolerance

        'target': list(set([0.010, -0.010, 0.020, -0.020, 0.030, -0.030, 0.040, -0.040, 0.050, -0.050, 0.060, -0.060, 0.070, -0.070, 0.080, -0.080, 0.090, -0.090, 0.100, -0.100, 0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.600,
                            0.015, -0.015, 0.030, -0.030, 0.045, -0.045, 0.060, -0.060, 0.075, -0.075, 0.090, -0.090, 0.105, -0.105, 0.120, -0.120, 0.135, -0.135, 0.150, -0.150, 0.225, 0.300, 0.375, 0.450, 0.600, 0.750, 0.900,
                            0.020, -0.020, 0.040, -0.040, 0.060, -0.060, 0.080, -0.080, 0.100, -0.100, 0.120, -0.120, 0.140, -0.140, 0.160, -0.160, 0.180, -0.180, 0.200, -0.200, 0.300, 0.400, 0.500, 0.600, 0.800, 1.000, 1.200,
                            0.030, -0.030, 0.060, -0.060, 0.090, -0.090, 0.120, -0.120, 0.150, -0.150, 0.180, -0.180, 0.210, -0.210, 0.240, -0.240, 0.270, -0.270, 0.300, -0.300, 0.450, 0.600, 0.750, 0.900, 1.200, 1.500, 1.800,
                            0.007, -0.007, 0.014, -0.014, 0.021, -0.021, 0.028, -0.028, 0.035, -0.035, 0.042, -0.042, 0.049, -0.049, 0.056, -0.056, 0.063, -0.063, 0.070, -0.070, 0.105, 0.140, 0.175, 0.210, 0.280, 0.350, 0.420,
                            0.011, -0.011, 0.022, -0.022, 0.033, -0.033, 0.044, -0.044, 0.055, -0.055, 0.066, -0.066, 0.077, -0.077, 0.088, -0.088, 0.099, -0.099, 0.110, -0.110, 0.165, 0.220, 0.275, 0.330, 0.440, 0.550, 0.660,
                            0.014, -0.014, 0.028, -0.028, 0.042, -0.042, 0.056, -0.056, 0.070, -0.070, 0.084, -0.084, 0.098, -0.098, 0.112, -0.112, 0.126, -0.126, 0.140, -0.140, 0.210, 0.280, 0.350, 0.420, 0.560, 0.700, 0.840,
                            0.018, -0.018, 0.036, -0.036, 0.054, -0.054, 0.072, -0.072, 0.090, -0.090, 0.108, -0.108, 0.126, -0.126, 0.144, -0.144, 0.162, -0.162, 0.180, -0.180, 0.270, 0.360, 0.450, 0.540, 0.720, 0.900, 1.080
                            ])),

        'nanmean': True,    # use nanmean to build population features, will ignore nan features
                            # this ignores the fact that some cells do not provide spikeshape features when they are not spiking
                            # this causes some conceptual troubles in the fitting: i.e./e.g. what is the action potential width of a cell that is not spiking?
        'nanmean_cell': True,
        "logging": True,  # print info
        "target_unit": "nA",
        "featconffile": "./pt_conf_mice.json",
        "zero_std": True,  # consider results even if std == 0
        "trace_check": False,  # if True exclude any activities outside stimulus
        "featzerotonan": True,  # convert the value of the features indicated in
                                # the array MEANFEATURES_NO_ZEROS of the featconffile (pt_conf.json),
                                # from zero to nan (when the efel computation returns zero).

        "print_table": {
            "flag": True,
            "num_events": 5,
        },
        "strict_stiminterval": {
            "base": True
        },
        "amp_min": -1e22,

        "steady_state_threshold": 30,       # in hz
        "remove_last_100ms": False,

        # new added features
        "correct_standard_currents_with_baseline_current": True,
        "remove_wrong_traces": True,
        "highfreq_firing_threshold": 150     # in hz
    },
}


import bluepyefe as bpefe

extractor = bpefe.Extractor('./PTI_PV_standard_features_MOUSE_expdata_FINAL_NEW', config)
# extractor = bpefe.Extractor('./PTI_PV_standard_features_MOUSE_expdata_without_r180605_03', config)


extractor.create_dataset()
extractor.create_metadataset()
extractor.plt_traces()
extractor.extract_features(threshold=-10)  # original is -20

extractor.collect_global_features()

extractor.mean_features()
extractor.plt_features()

extractor.feature_config_cells()
extractor.feature_config_all()
