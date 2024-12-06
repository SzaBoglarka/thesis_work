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
dt_rat_somaaxon = 1/int(100000) * 1e3
dt_rat_somadend = 1/int(40000) * 1e3


config = {
    'features': {
        'step':[
    "all_ISI_values",
    "Spikecount_stimint",
    "time_to_first_spike"
    #"inv_ISI_values"
    #    "peak_time", already added in extractor.py
    ]
    },
    'path': '/home/szabobogi/Documents/Hu_rat_hippocampus_data/KOKI_format_FINAL/',
    'format': 'csv_lccr',
    # 'comment':  [],


    'cells': {

	'HH0806190AB':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH0806190AB_ch1'], 'baseline_currents': [0.02], 'wrong_traces': [[]], 'dt':dt_rat_somadend, 'startstop':[610.2,1610.0], 'amplitudes': [-0.180, -0.130, -0.080, -0.030, 0.020, 0.070, 0.120, 0.170, 0.220, 0.270, 0.320, 0.370, 0.420, 0.470, 0.520, 0.570, 0.620, 0.670, 0.720, 0.770], 'hypamp': 0.0,'ton':610.2, 'toff':1610.0}}},

	#'HH0804170AA':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH0804170AA_ch1'], 'dt':dt_rat_somadend, 'startstop':[610.2,1610.0], 'amplitudes': [-0.18, -0.13, -0.08, -0.03, 0.02, 0.07, 0.12, 0.17, 0.22, 0.27, 0.32, 0.37, 0.42, 0.47, 0.52, 0.57, 0.62, 0.67, 0.72, 0.77], 'hypamp': 0.0,'ton':610.2, 'toff':1610.0}}},

	'HH180618_0001':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH180618_0001_ch3'], 'baseline_currents': [0.00], 'wrong_traces': [[]], 'dt':dt_rat_somaaxon, 'startstop':[123.55,1123.42], 'amplitudes': [-0.300, -0.200, -0.100, 0.000, 0.100, 0.200, 0.300, 0.400, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000], 'hypamp': 0.0,'ton':123.55, 'toff':1123.42}}},

	'HH0804220AB':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH0804220AB_ch1'], 'baseline_currents': [0.023], 'wrong_traces': [[]], 'dt':dt_rat_somadend, 'startstop':[610.2,1610.0], 'amplitudes': [-0.180, -0.130, -0.080, -0.030, 0.020, 0.070, 0.120, 0.170, 0.220, 0.270, 0.320, 0.370, 0.420, 0.470, 0.520, 0.570, 0.620, 0.670, 0.720, 0.770], 'hypamp': 0.0,'ton':610.2, 'toff':1610.0}}},

	'HH0805230AI':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH0805230AI_ch1'], 'baseline_currents': [-0.13], 'wrong_traces': [[]], 'dt':dt_rat_somadend, 'startstop':[610.2,1610.0], 'amplitudes': [-0.180, -0.130, -0.080, -0.030, 0.020, 0.070, 0.120, 0.170, 0.220, 0.270, 0.320, 0.370, 0.420, 0.470, 0.520, 0.570, 0.620, 0.670, 0.720, 0.770], 'hypamp': 0.0,'ton':610.2, 'toff':1610.0}}},

	'HH0805130AP':{'v_corr':False, 'ljp':0, 'experiments':{'step': {'location':'soma', 'files':['HH0805130AP_ch1'], 'baseline_currents': [0.12], 'wrong_traces': [[20]], 'dt':dt_rat_somadend, 'startstop':[610.2,1610.0], 'amplitudes': [-0.180, -0.130, -0.080, -0.030, 0.020, 0.070, 0.120, 0.170, 0.220, 0.270, 0.320, 0.370, 0.420, 0.470, 0.520, 0.570, 0.620, 0.670, 0.720, 0.770], 'hypamp': 0.0,'ton':610.2, 'toff':1610.0}}},

    },


    'options': {
        'relative': False,  # is the target given relative or in absolute current?

        'tolerance': 0.0001,  # group features based on target +/- this tolerance

        'target': [-0.180, -0.130, -0.080, -0.030, 0.020, 0.070, 0.120, 0.170, 0.220, 0.270, 0.320, 0.370, 0.420, 0.470, 0.520, 0.570, 0.620, 0.670, 0.720, 0.770,
                   -0.300, -0.200, -0.100, 0.000, 0.100, 0.200, 0.300, 0.400, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000],  # support for grouping features

        'nanmean': True,    # use nanmean to build population features, will ignore nan features
                            # this ignores the fact that some cells do not provide spikeshape features when they are not spiking
                            # this causes some conceptual troubles in the fitting: i.e./e.g. what is the action potential width of a cell that is not spiking?
        'nanmean_cell': True,
        "logging": True,  # print info
        "target_unit": "nA",
        "featconffile": "./pt_conf_mice.json",
        "zero_std": True,  # consider results even if std == 0
        "trace_check": False,  # if True exclude any activities outside stimulus
        "featzerotonan": True,      # convert the value of the features indicated in
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

        # for this use-case we will need the original current amplitudes
        # BUT on the figures if we will plot the amplitudes as well we should
        # correct them with the baseline current !!!
        "correct_standard_currents_with_baseline_current": False,
        "remove_wrong_traces": True,
        "highfreq_firing_threshold": 150     # in hz
    },
}


import bluepyefe as bpefe

extractor = bpefe.Extractor('./feat_extr_RAT_expdata', config)

extractor.create_dataset()
extractor.create_metadataset()
extractor.plt_traces()
extractor.extract_features(threshold=-10)  # original is -20

extractor.collect_global_features()

extractor.mean_features()
extractor.plt_features()

extractor.feature_config_cells()
extractor.feature_config_all()
