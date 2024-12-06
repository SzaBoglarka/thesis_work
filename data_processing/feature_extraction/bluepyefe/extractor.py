"""Extractor class"""
import warnings

"""
Copyright (c) 2020, EPFL/Blue Brain Project

 This file is part of BluePyEfe <https://github.com/BlueBrain/BluePyEfe>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import matplotlib
matplotlib.use('Agg')  # noqa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy
import sys
import efel
import os
import logging
import gzip
import json
import pprint

from itertools import cycle
from collections import OrderedDict
from collections import defaultdict

from . import tools
from .tools import tabletools
from . import plottools
from . import extra
from .formats import common


logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()


# class Extractor(object):
class Extractor(object):

    """Extractor class"""

    def __init__(self, mainname='PC', config=OrderedDict()):
        """Constructor

        Args:
            mainname (str): name of the cell type. Used to create the output
            directory
            config (dict): metadata containing the protocols and cells for
            which to extract the efeatures.
        """

        self.config = config
        self.path = config['path']
        self.cells = config['cells']
        self.features = config['features']
        self.options = config['options']

        for experiment in self.features:
            f = self.features[experiment]
            self.features[experiment] = sorted(
                set(f), key=lambda x: f.index(x))

        self.format = config['format']

        self.dataset = OrderedDict()
        self.dataset_mean = OrderedDict()

        self.max_per_plot = 16

        conv_fact = 1

        if "relative" not in self.options:
            self.options["relative"] = False

        if "amp_min" not in self.options:
            self.options["amp_min"] = 0.001  # minimum current amplitude used

        if "peak_min" not in self.options:
            # minimum current amplitude used for spike detection
            self.options["peak_min"] = 0.001

        if "target" not in self.options:
            self.options["target"] = [100., 150., 200., 250.]
        else:
            if "target_unit" in self.options:
                target_unit = self.options["target_unit"].lower()
                conv_fact = common.manageConfig.conversion_factor(
                    'nA', target_unit)
                if conv_fact != 1:
                    conv_target = [
                        i * conv_fact for i in
                        self.options["target"]]
                    self.options["target"] = conv_target

        if "tolerance" not in self.options:
            self.options["tolerance"] = 10

        if "strict_stiminterval" not in self.options:
            self.options["strict_stiminterval"] = {'base': False}

        if isinstance(self.options["tolerance"], list) is False:
            if conv_fact != 1:
                tolerance = self.options["tolerance"]
                self.options["tolerance"] = conv_fact * tolerance
            self.options["tolerance"] =\
                numpy.ones(len(self.options["target"]))\
                * self.options["tolerance"]
        elif conv_fact != 1:
            self.options["tolerance"] = \
                [x * conv_fact for x in self.options["tolerance"]]

        if "nanmean" not in self.options:
            self.options["nanmean"] = False

        if "nanmean_cell" not in self.options:
            self.options["nanmean_cell"] = True

        if "nangrace" not in self.options:
            self.options["nangrace"] = 0

        if "delay" not in self.options:
            self.options["delay"] = 0

        if "posttime" not in self.options:
            self.options["posttime"] = 200

        if "spike_threshold" not in self.options:
            self.options["spike_threshold"] = 2

        # in this extractor version the steady_state_threshold is a frequency (Hz)
        if "steady_state_threshold" not in self.options:
            self.options["steady_state_threshold"] = 8

        if "remove_last_100ms" not in config["options"]:
            config["options"]["remove_last_100ms"] = True

        if "logging" not in self.options:
            self.options["logging"] = False

        if self.options["logging"]:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.ERROR)

        self.saveraw = False
        if ('saveraw' in self.options) and self.options['saveraw']:
            self.saveraw = True

        self.colors = OrderedDict()
        self.colors['b1'] = '#1F78B4'  # 377EB8
        self.colors['b2'] = '#A6CEE3'
        self.colors['g1'] = '#33A02C'  # 4DAF4A
        self.colors['g2'] = '#B2DF8A'
        self.colors['r1'] = '#E31A1C'  # E41A1C
        self.colors['r2'] = '#FB9A99'
        self.colors['o1'] = '#FF7F00'  # FF7F00
        self.colors['o2'] = '#FDBF6F'
        self.colors['p1'] = '#6A3D9A'  # 984EA3
        self.colors['p2'] = '#CAB2D6'
        self.colors['ye1'] = '#FFFF33'
        self.colors['br1'] = '#A65628'
        self.colors['pi1'] = '#F781BF'
        self.colors['gr1'] = '#999999'
        self.colors['k1'] = '#000000'

        self.markerlist = ['o', '*', '^', 'H', 'D', 's', 'p', '.', '8', '+']
        self.colorlist = [
            self.colors['b1'],
            self.colors['g1'],
            self.colors['r1'],
            self.colors['o1'],
            self.colors['p1'],
            self.colors['ye1']]
        self.experiments = []

        self.mainname = mainname
        self.maindirname = mainname + os.sep  # llb
        tools.makedir(self.maindirname)

        self.thresholds_per_cell = OrderedDict()
        self.hypamps_per_cell = OrderedDict()

        self.extra_features = ['spikerate_tau_jj', 'spikerate_drop',
                               'spikerate_tau_log', 'spikerate_tau_fit',
                               'spikerate_tau_slope']

        if "standard_negative_current" not in self.options:
            self.options["standard_negative_current"] = -0.1  # -100 pA, default standard negative current value
        self.standard_currents = ['rheobase_current', 'rheobase_prev_current', 'steady_state_current',
                                  'highfreq_firing_current', 'standard_negative_current']
        self.global_features = ['initial_fI_slope', 'average_fI_slope', 'maximum_fI_slope']
        self.is_global_features_collected = False

        # default value is False
        self.remove_wrong_traces = self.options.get("remove_wrong_traces", False)

        # default value is False
        self.correct_standard_currents_with_baseline_current = self.options.get(
            "correct_standard_currents_with_baseline_current", False)

        # default value is True
        self.use_maxspike_as_high_freq_curr = self.options.get("highfreq_firing_threshold", True)

        # default value is False
        self.highfreq_firing_threshold = self.options.get("highfreq_firing_threshold", None)
        if self.highfreq_firing_threshold:
            self.use_maxspike_as_high_freq_curr = False

    def newmeancell(self, a):
        if (self.options["nanmean_cell"] or
                (numpy.sum(numpy.isnan(a)) <= self.options["nangrace"])):
            return numpy.nanmean(a)
        else:
            return numpy.mean(a)

    def newstdcell(self, a):
        if (self.options["nanmean_cell"] or
                (numpy.sum(numpy.isnan(a)) <= self.options["nangrace"])):
            return numpy.nanstd(a)
        else:
            return numpy.std(a)

    def boxcoxcell(self, a, nanopt="nanmean_cell",
                   lm_vec=numpy.linspace(-3, 3, 41)):
        if ((self.options[nanopt] or
             (numpy.sum(numpy.isnan(a)) <= self.options["nangrace"])) and
                (len(a) > 0)):
            a = numpy.array(a)
            a = a[~numpy.isnan(a)]
        else:
            return float('NaN'), float('NaN'), float('NaN'), float('NaN')

        return float('NaN'), float('NaN'), float('NaN'), float('NaN')

    def newmean(self, a):
        if (self.options["nanmean"] or
                (numpy.sum(numpy.isnan(a)) <= self.options["nangrace"])):
            return numpy.nanmean(a)
        else:
            return numpy.mean(a)

    def newstd(self, a):
        if (self.options["nanmean"] or
                (numpy.sum(numpy.isnan(a)) <= self.options["nangrace"])):
            return numpy.nanstd(a)
        else:
            return numpy.std(a)

    def create_dataset(self):
        """Read the trace files and add them to the dictionnary self.dataset"""
        logger.info(" Filling dataset")

        for i_cell, cellname in enumerate(self.cells):

            self.dataset[cellname] = OrderedDict()

            v_corr = self.cells[cellname]['v_corr']
            self.dataset[cellname]['v_corr'] = v_corr

            if 'ljp' in self.cells[cellname]:
                ljp = self.cells[cellname]['ljp']
            else:
                ljp = 0
            self.dataset[cellname]['ljp'] = ljp

            dataset_cell_exp = OrderedDict()
            self.dataset[cellname]['experiments'] = dataset_cell_exp

            for i_exp, expname in enumerate(
                    self.cells[cellname]['experiments']):

                files = self.cells[cellname]['experiments'][expname]['files']

                # read stimulus features if present
                stim_feats = []
                if 'stim_feats' in self.cells[cellname]['experiments'][
                        expname]:
                    stim_feats = \
                        self.cells[cellname][
                            'experiments'][expname]['stim_feats']

                # read baseline currents if needed
                if self.correct_standard_currents_with_baseline_current:
                    if 'baseline_currents' in self.cells[cellname]['experiments'][expname]:
                        baseline_currents = self.cells[cellname]['experiments'][expname]['baseline_currents']
                        if not len(files) == len(baseline_currents):
                            raise ValueError(
                                "Mismatch between the number of files (%s) and baseline currents (%s) in cell '%s'." % 
                                (len(files), len(baseline_currents), cellname)
                            )
                    else:
                        raise KeyError(f"'baseline_currents' not found in experiment '{expname}' for cell '{cellname}'.")

                # read wrong trace indices if needed
                if self.remove_wrong_traces:
                    if 'wrong_traces' in self.cells[cellname]['experiments'][expname]:
                        wrong_traces = self.cells[cellname]['experiments'][expname]['wrong_traces']
                        if not len(files) == len(wrong_traces):
                            raise ValueError(
                                "Mismatch between the number of files (%s) and wrong_traces (%s) in cell '%s'." %
                                (len(files), len(wrong_traces), cellname)
                            )
                    else:
                        raise KeyError(f"'wrong_traces' not found in experiment '{expname}' for cell '{cellname}'.")


                if len(files) > 0:
                    logger.debug(" Adding experiment %s", expname)

                    if expname not in self.experiments:
                        self.experiments.append(expname)

                    dataset_cell_exp[expname] = OrderedDict()

                    dataset_cell_exp[expname]['location'] = \
                        self.cells[cellname][
                        'experiments'][expname]['location']

                    dataset_cell_exp[expname]['voltage'] = []
                    dataset_cell_exp[expname]['current'] = []
                    dataset_cell_exp[expname]['dt'] = []
                    dataset_cell_exp[expname]['filename'] = []

                    dataset_cell_exp[expname]['t'] = []
                    dataset_cell_exp[expname]['ton'] = []
                    dataset_cell_exp[expname]['tend'] = []
                    dataset_cell_exp[expname]['toff'] = []
                    dataset_cell_exp[expname]['amp'] = []
                    dataset_cell_exp[expname]['hypamp'] = []
                    dataset_cell_exp[expname]['files'] = []
                    dataset_cell_exp[expname]['rawfiles'] = []

                    for idx_file, filename in enumerate(files):

                        if self.remove_wrong_traces:
                            wrong_traces_file = wrong_traces[idx_file]
                        else:
                            wrong_traces_file = []

                        data = self.process_file(config=self.config,
                                                 filename=filename,
                                                 cellname=cellname,
                                                 expname=expname,
                                                 stim_feats=stim_feats,
                                                 idx_file=idx_file,
                                                 v_corr=v_corr,
                                                 ljp=ljp,
                                                 wrong_traces=wrong_traces_file)

                        dataset_cell_exp[expname]['voltage'] += data['voltage']
                        dataset_cell_exp[expname]['current'] += data['current']
                        dataset_cell_exp[expname]['dt'] += data['dt']
                        dataset_cell_exp[expname]['filename'] += \
                            data['filename']
                        dataset_cell_exp[expname]['rawfiles'].append(filename)

                        dataset_cell_exp[expname]['t'] += data['t']
                        dataset_cell_exp[expname]['ton'] += data['ton']
                        dataset_cell_exp[expname]['tend'] += data['tend']
                        dataset_cell_exp[expname]['toff'] += data['toff']
                        dataset_cell_exp[expname]['amp'] += data['amp']
                        dataset_cell_exp[expname]['hypamp'] += data['hypamp']

                    if self.correct_standard_currents_with_baseline_current:
                        dataset_cell_exp[expname]['baseline_currents'] = baseline_currents

    def process_file(self, **kwargs):
        """Get data from a trace file"""
        if self.format == 'igor':
            from .formats import igor
            return igor.process(**kwargs)
        elif self.format == 'axon':
            from .formats import axon
            return axon.process(**kwargs)
        elif self.format == 'csv_lccr':
            from .formats import csv_lccr
            return csv_lccr.process(**kwargs)
        elif self.format == 'spike2':
            from .formats import spike2
            return spike2.process(**kwargs)
        elif self.format == 'ibf_json':
            from .formats import ibf_json
            return ibf_json.process(**kwargs)
        else:
            raise ValueError('Unrecognized trace format: %s' % self.format)

    def plt_traces(self):
        """Plot traces"""
        logger.info(" Plotting traces")

        for i_cell, cellname in enumerate(self.dataset):

            dirname = self.maindirname + cellname
            tools.makedir(dirname)
            dataset_cell_exp = self.dataset[cellname]['experiments']

            for i_exp, expname in enumerate(dataset_cell_exp):

                voltages = dataset_cell_exp[expname]['voltage']
                currents = dataset_cell_exp[expname]['current']
                amps = dataset_cell_exp[expname]['amp']
                ts = dataset_cell_exp[expname]['t']
                filenames = dataset_cell_exp[expname]['filename']

                colors = []

                colorcycler = cycle(self.colorlist)

                color_dict = {u: next(colorcycler)
                              for u in list(set(filenames))}
                colors = [color_dict[f] for f in filenames]

                isort = numpy.argsort(amps)
                amps = numpy.array(amps)[isort]
                ts = numpy.array(ts)[isort]
                voltages = numpy.array(voltages)[isort]
                currents = numpy.array(currents)[isort]
                colors = numpy.array(colors)[isort]
                filenames = numpy.array(filenames)[isort]

                n_plot = len(voltages)

                if n_plot <= self.max_per_plot:
                    frames = n_plot
                    n_fig = 1
                else:
                    frames = self.max_per_plot
                    n_fig = int(numpy.ceil(n_plot / float(self.max_per_plot)))

                axs = []
                figs = OrderedDict()

                axs_c = []
                figs_c = OrderedDict()

                for i_fig in range(n_fig):
                    figname = cellname.split(
                        '/')[-1] + "_" + expname + "_" + str(i_fig)
                    axs = plottools.tiled_figure(
                        figname, frames=frames, columns=2, figs=figs, axs=axs,
                        top=0.97, bottom=0.04, left=0.07, right=0.97,
                        hspace=0.75, wspace=0.2)

                    figname_c = cellname.split(
                        '/')[-1] + "_" + expname + "_" + str(i_fig) + "_i"
                    axs_c = plottools.tiled_figure(
                        figname_c, frames=frames, columns=2, figs=figs_c,
                        axs=axs_c, top=0.97, bottom=0.04, left=0.07,
                        right=0.97, hspace=0.75, wspace=0.2)

                for i_plot in range(n_plot):
                    # reduce figure title length if too long
                    filename_string = filenames[i_plot]
                    if len(filename_string) > 50:
                        filename_fin = filename_string[:18] + ' ... ' + \
                            filename_string[-18:]
                    else:
                        filename_fin = filename_string

                    axs[i_plot].plot(
                        ts[i_plot],
                        voltages[i_plot],
                        color=colors[i_plot],
                        clip_on=False)
                    axs[i_plot].set_title(
                        cellname + " " + expname + " amp:" +
                        str(amps[i_plot]) +
                        " file:" + filename_fin)

                    axs_c[i_plot].plot(
                        ts[i_plot],
                        currents[i_plot],
                        color=colors[i_plot],
                        clip_on=False)
                    axs_c[i_plot].set_title(
                        cellname + " " + expname + " amp:" +
                        str(amps[i_plot]) +
                        " file:" + filename_fin)

                # plt.show()

                for i_fig, figname in enumerate(figs):
                    fig = figs[figname]
                    fig['fig'].savefig(
                        dirname + '/' + figname + '.pdf', dpi=300)
                    plt.close(fig['fig'])

                for i_fig, figname in enumerate(figs_c):
                    fig = figs_c[figname]
                    fig['fig'].savefig(
                        dirname + '/' + figname + '.pdf', dpi=300)
                    plt.close(fig['fig'])

    def extract_features(self, threshold=-20):
        """Extract features from the traces"""
        logger.info(" Extracting features")

        efel.setThreshold(threshold)
        logger.info(" Setting spike threshold to %.2f mV", threshold)


        # if print_table flag is set, dump all extracted feature to a .csv file
        print_table_flag = False
        if 'print_table' in self.options and self.options[
                'print_table']['flag']:
            print_table_flag = True
            all_feat_filename = os.path.join(
                self.mainname, 'all_feature_table.txt')
            if os.path.exists(all_feat_filename):
                os.remove(all_feat_filename)
            if not hasattr(self, "metadataset"):
                self.create_metadataset()

        # set flag to convert zero value to nan for features set by the user
        if 'zero_to_nan' in self.options and \
                'flag' in self.options['zero_to_nan']:
            ZERO_TO_NAN = self.options['zero_to_nan']['flag']
        else:
            ZERO_TO_NAN = False

        for i_cell, cellname in enumerate(self.dataset):
            dataset_cell_exp = self.dataset[cellname]['experiments']
            for i_exp, expname in enumerate(dataset_cell_exp):

                if expname in self.options["strict_stiminterval"].keys():
                    strict_stiminterval = self.options["strict_stiminterval"][
                        expname]
                else:
                    strict_stiminterval = self.options["strict_stiminterval"][
                        'base']
                efel.setIntSetting("strict_stiminterval", strict_stiminterval)

                ts = dataset_cell_exp[expname]['t']
                voltages = dataset_cell_exp[expname]['voltage']
                tons = dataset_cell_exp[expname]['ton']
                toffs = dataset_cell_exp[expname]['toff']
                amps = dataset_cell_exp[expname]['amp']

                features_all = self.features[expname] + ['peak_time']

                if 'threshold' in self.cells[cellname]['experiments'][expname]:
                    threshold = self.cells[cellname][
                        'experiments'][expname]['threshold']
                    logger.info(" Setting threshold to %f", threshold)
                    efel.setThreshold(threshold)

                dataset_cell_exp[expname]['features'] = OrderedDict()
                for feature in features_all:
                    dataset_cell_exp[expname]['features'][feature] = []
                dataset_cell_exp[expname]['features']['numspikes'] = []

                # iterate over all voltages individually to get features
                # and correct them if needed
                for i_seg in range(len(voltages)):

                    trace = OrderedDict()
                    trace['T'] = ts[i_seg]
                    trace['V'] = voltages[i_seg]
                    trace['stim_start'] = [tons[i_seg]]
                    trace['stim_end'] = [toffs[i_seg]]
                    traces = [trace]
                    amp = amps[i_seg]

                    efel.setDoubleSetting('stimulus_current', amp)

                    features_all_ = [
                        f for f in features_all
                        if f not in self.extra_features]

                    fel_vals = efel.getFeatureValues(
                        traces, features_all_, raise_warnings=False)

                    #correction for AP1 detection error
                    for key in fel_vals[0]:
                       if fel_vals[0][key] is not None and fel_vals[0][key].size !=0:
                           if (key == 'AP_rise_time' or key == 'AP_amplitude' or key == 'AP_duration_half_width' or key == 'AP_begin_voltage'
                               or key == 'AP_rise_rate' or key == 'fast_AHP' or key == 'AP_begin_time' or key == 'AP_begin_width' or key == 'AP_duration'
                               or key == 'AP_duration_change' or key == 'AP_duration_half_width_change' or key == 'fast_AHP_change' or key == 'AP_rise_rate_change' or key == 'AP_width'):
                               feature_name_for_corr = fel_vals[0][key]
                               corrected_feature = feature_name_for_corr[1:]
                               fel_vals[0][key] = corrected_feature

                    peak_times = fel_vals[0]['peak_time']

                    for feature in features_all:

                        if feature == 'peak_time':
#                            if (len(peak_times) >
#                                    0) and amp >= self.options["peak_min"]:
                            if (peak_times is not None) and amp >= self.options["peak_min"]:
                                numspike = len(peak_times)
                            else:
                                numspike = 0

                        elif feature == 'spikerate_tau_jj':
                            if len(peak_times) > 4:
                                f = extra.spikerate_tau_jj(peak_times)
                            else:
                                f = None

                        elif feature == 'spikerate_drop':
                            if len(peak_times) > 4:
                                f = extra.spikerate_drop(peak_times)
                            else:
                                f = None

                        elif feature == 'spikerate_tau_log':
                            if len(peak_times) > 4:
                                f = extra.spikerate_tau_log(peak_times)
                            else:
                                f = None

                        elif feature == 'spikerate_tau_fit':
                            if len(peak_times) > 4:
                                f = extra.spikerate_tau_fit(peak_times)
                            else:
                                f = None

                        elif feature == 'spikerate_tau_slope':
                            if len(peak_times) > 4:
                                f = extra.spikerate_tau_slope(peak_times)
                            else:
                                f = None
                        elif fel_vals[0][feature] is not None and \
                                len(fel_vals[0][feature]) == 1 and \
                                fel_vals[0][feature][0] == 0 and ZERO_TO_NAN \
                                and feature in self.options[
                                    'zero_to_nan'][
                                    'mean_features_no_zeros']:
                            if self.options[
                                    'zero_to_nan']['value'] == 'stim_end':
                                fel_vals[0][feature] = [toffs[i_seg]]
                                f = [toffs[i_seg]]
                            elif self.options[
                                    'zero_to_nan']['value'] == 'nan':
                                fel_vals[0][feature] = None
                                f = None
                            else:
                                logger.info(
                                    "Unrecognized value " +
                                    "for zero_to_nan option")
                        else:
                            f = fel_vals[0][feature]

                        if abs(amp) < self.options["amp_min"]:
                            f = float('nan')
                        elif f is not None:
                            f = numpy.mean(f)
                        else:
                            f = float('nan')

                        if "trace_check" in self.options and \
                                self.options["trace_check"] is False:
                            pass
                        else:
                            # exclude any activity outside stimulus (20 ms
                            # grace period)
                            if (any(numpy.atleast_1d(peak_times) < trace['stim_start'][0]) or
                                    any(numpy.atleast_1d(peak_times) > trace['stim_end'][0] + 20)):
                                f = float('nan')

                        dataset_cell_exp[expname]['features'][feature].append(
                            f)

                    dataset_cell_exp[expname]['features']['numspikes'].append(
                        numspike)

                    # Print individual features to table if required
                    if print_table_flag:

                        crr_filename = dataset_cell_exp[
                            expname]['filename'][i_seg]
                        all_feat_filename = os.path.join(
                            self.mainname, 'all_feature_table.txt')
                        if 'num_events' not in self.options['print_table']:
                            multvalnum = 5
                        else:
                            multvalnum = self.options['print_table'][
                                'num_events']
                        tabletools.printFeatures.dump_features(
                            all_feat_filename=all_feat_filename,
                            cellname=cellname,
                            trace_filename=crr_filename,
                            features_name=features_all_,
                            fel_vals=fel_vals,
                            multvalnum=multvalnum,
                            metadata=self.metadataset[
                                cellname]['experiments'][
                                    expname][crr_filename],
                            amp=amp,
                            stim_start=trace['stim_start'][0],
                            stim_end=trace['stim_end'][0],
                        )

                # collect number of spikes for each current injection
                currents_spikecounts = defaultdict(OrderedDict)
                for idx, filename in enumerate(dataset_cell_exp[expname]['filename']):
                    numspike = dataset_cell_exp[expname]['features']['Spikecount_stimint'][idx]
                    current = dataset_cell_exp[expname]['amp'][idx]
                    currents_spikecounts[filename][current] = numspike
                self.dataset[cellname]['experiments'][expname]['currents_spikecounts'] = currents_spikecounts

    def collect_global_features(self):
        self.is_global_features_collected = True
        steady_state_threshold = self.options["steady_state_threshold"]

        for i_cell, cellname in enumerate(self.dataset):
            dataset_cell_exp = self.dataset[cellname]['experiments']
            for i_exp, expname in enumerate(dataset_cell_exp):
                if 'currents_spikecounts' not in dataset_cell_exp[expname]:
                    logging.info('Features must be collected before features for rheobase, steady-state current' +
                                 ' or current with max number of spikes can be collected.')
                    continue

                if 'global_features' not in self.dataset[cellname]['experiments'][expname]:
                    self.dataset[cellname]['experiments'][expname]['global_features'] = {}

                ton = self.dataset[cellname]['experiments'][expname]['ton'][0]
                toff = self.dataset[cellname]['experiments'][expname]['toff'][0]
                delta_t = toff - ton

                amplitudes = self.cells[cellname]['experiments'][expname]['amplitudes']
                filenames = set(dataset_cell_exp[expname]['filename'])
                for i_file, filename in enumerate(filenames):
                    currents_spikecounts = dataset_cell_exp[expname]['currents_spikecounts'][filename]
                    currents_spikecounts_sorted = sorted(currents_spikecounts.items(), key=lambda elem: float(elem[0]))

                    # select feature values coming from the current file
                    file_indices = []
                    for j_file, dummy_filename in enumerate(dataset_cell_exp[expname]['filename']):
                        if dummy_filename == filename:
                            file_indices.append(j_file)
                    file_features = OrderedDict()
                    for feature in self.dataset[cellname]['experiments'][expname]['features']:
                        feature_values = self.dataset[cellname]['experiments'][expname]['features'][feature]
                        for index in file_indices:
                            if feature not in file_features:
                                file_features[feature] = []
                            file_features[feature].append(feature_values[index])

                    # find rheobase and steady state currents
                    current_dict = defaultdict(dict)
                    for current_name in self.standard_currents:
                        current_dict[current_name]['current'] = float('nan')
                        current_dict[current_name]['index'] = -1

                    delta_t_sec = delta_t / 1000
                    for current, spikecount in currents_spikecounts_sorted:
                        if spikecount != 0 and current_dict['rheobase_current']['index'] == -1:
                            current_dict['rheobase_current']['current'] = current
                            current_dict['rheobase_current']['index'] = list(currents_spikecounts).index(current)
                        if (spikecount / delta_t_sec) >= steady_state_threshold and current_dict['steady_state_current']['index']  == -1:
                            current_dict['steady_state_current']['current'] = current
                            current_dict['steady_state_current']['index'] = list(currents_spikecounts).index(current)

                    # find current just below rheobase (rheobase_prev_current)
                    if current_dict['rheobase_current']['index'] != 0:
                        current_dict['rheobase_prev_current']['index'] = current_dict['rheobase_current']['index'] - 1
                        current_dict['rheobase_prev_current']['current'] = currents_spikecounts_sorted[current_dict['rheobase_prev_current']['index']][0]
                    else:
                        logging.info("Rheobase at smallest injected current; current below rheobase cannot be calculated.")

                    if self.use_maxspike_as_high_freq_curr:
                        # find current with the largest number of spikes (maxspike)
                        spikecounts = currents_spikecounts.values()
                        if any(spikecounts):
                            maxspike_current, _ = list(
                                filter(lambda current_spikecount_tuple: current_spikecount_tuple[1] == max(spikecounts),
                                       currents_spikecounts_sorted))[0]
                            current_dict['highfreq_firing_current']['current'] = maxspike_current
                            current_dict['highfreq_firing_current']['index'] = list(currents_spikecounts).index(
                                maxspike_current)

                    else:
                        # find current that first exceeds the threshold (or if it don't use the max-spike current)
                        spikecounts = currents_spikecounts.values()
                        if any(spikecounts):
                            max_spikecount = -1
                            delta_t_sec = delta_t / 1000
                            threshold_exceeded = False

                            for current, spikecount in currents_spikecounts_sorted:
                                frequency_hz = spikecount / delta_t_sec
                                # Check if the frequency is equal to or exceeds the threshold
                                if frequency_hz >= self.highfreq_firing_threshold:
                                    highfreq_firing_current = current
                                    threshold_exceeded = True
                                    break  # Stop as soon as it does
                                # Track the maximum spikecount in case no frequency meets the threshold
                                if spikecount > max_spikecount:
                                    max_spikecount = spikecount
                                    highfreq_firing_current = current

                            if threshold_exceeded:
                                current_dict['highfreq_firing_current']['current'] = highfreq_firing_current
                                current_dict['highfreq_firing_current']['index'] = list(
                                    currents_spikecounts).index(highfreq_firing_current)

                            else:
                                print(f"Experiment {filename} did not exceed the frequency threshold of {self.highfreq_firing_threshold}")
                                print(f"Using the current {highfreq_firing_current} with the maximum firing frequency: {max_spikecount / delta_t_sec}")
                                current_dict['highfreq_firing_current']['current'] = highfreq_firing_current
                                current_dict['highfreq_firing_current']['index'] = list(
                                    currents_spikecounts).index(highfreq_firing_current)

                    # find standardized negative current
                    if self.options["standard_negative_current"] in amplitudes:
                        current_dict['standard_negative_current']['current'] = self.options["standard_negative_current"]
                        current_dict['standard_negative_current']['index'] = amplitudes.index(self.options["standard_negative_current"])
                    else: # find closest alternative to std neg curr
                        distances_from_stdneg_curr = numpy.abs([amplitude - self.options["standard_negative_current"] for amplitude in amplitudes])
                        closest_alternative_index = numpy.argmin(distances_from_stdneg_curr)
                        current_dict['standard_negative_current']['current'] = amplitudes[closest_alternative_index]
                        current_dict['standard_negative_current']['index'] = closest_alternative_index
                        logging.log(logging.INFO, "Standard negative current of {} not found for {}. Using closest alternative of {}.".format(
                            self.options['standard_negative_current'], filename, amplitudes[closest_alternative_index]
                        ))

                    # collect features into dataset
                    for current_name in self.standard_currents:
                        if current_name not in self.dataset[cellname]['experiments'][expname]:
                            self.dataset[cellname]['experiments'][expname][current_name] = defaultdict(dict)
                        current_index = current_dict[current_name]['index']
                        if current_index >= 0:
                            current_features = OrderedDict()
                            for feature in file_features:
                                current_features[feature] = file_features[feature][current_index]
                            if filename not in self.dataset[cellname]['experiments'][expname][current_name]:
                                self.dataset[cellname]['experiments'][expname][current_name][filename] = {}
                            self.dataset[cellname]['experiments'][expname][current_name][filename]['current'] = current_dict[current_name]['current']
                            self.dataset[cellname]['experiments'][expname][current_name][filename]['features'] = current_features
                        else:
                            self.dataset[cellname]['experiments'][expname][current_name][filename] = current_dict

                    # calculate slope features
                    if 'features' in self.dataset[cellname]['experiments'][expname]['rheobase_current'][filename]:
                        rheobase_current = current_dict['rheobase_current']['current']
                        steady_state_current = current_dict['steady_state_current']['current']
                        highfreq_firing_current = current_dict['highfreq_firing_current']['current']
                        rheobase_spikecount = self.dataset[cellname]['experiments'][expname]['rheobase_current'][filename]['features']['Spikecount_stimint']
                        self.dataset[cellname]['experiments'][expname]['global_features'][filename] = {}

                        # "normal case"
                        if not numpy.isnan(steady_state_current) and rheobase_current != steady_state_current and rheobase_current != highfreq_firing_current:
                            # calculate initial slope
                            if 'features' in self.dataset[cellname]['experiments'][expname]['steady_state_current'][filename]:
                                steady_state_spikecount = self.dataset[cellname]['experiments'][expname]['steady_state_current'][filename]['features']['Spikecount_stimint']
                                firing_rate = (steady_state_spikecount - rheobase_spikecount) / delta_t
                                initial_slope = firing_rate / (steady_state_current - rheobase_current)
                                self.dataset[cellname]['experiments'][expname]['global_features'][filename]['initial_fI_slope'] = initial_slope

                            # calculate average slope
                            if 'features' in self.dataset[cellname]['experiments'][expname]['highfreq_firing_current'][filename]:
                                maxspike_spikecount = self.dataset[cellname]['experiments'][expname]['highfreq_firing_current'][filename]['features']['Spikecount_stimint']
                                firing_rate = (maxspike_spikecount - rheobase_spikecount) / delta_t
                                average_slope = firing_rate / (highfreq_firing_current - rheobase_current)
                                self.dataset[cellname]['experiments'][expname]['global_features'][filename]['average_fI_slope'] = average_slope
                        else:  # edge cases: when the rheobase is equal to steady state or maximum spike current
                            # first we need to check if there is any current greater than the rheobase
                            rheobase_index = [stimulus for (stimulus, spikecount) in currents_spikecounts_sorted].index(rheobase_current)
                            rheobase_is_last = False
                            if rheobase_index + 1 == len(currents_spikecounts_sorted):
                                rheobase_is_last = True

                            if not rheobase_is_last:  # if there is a current greater than that, then we use that one for slope calculation
                                adjacent_current, adjacent_current_spikecount = currents_spikecounts_sorted[rheobase_index + 1]
                            else:  # if such a current doesn't exist, we step back and use the one immediately smaller
                                adjacent_current, adjacent_current_spikecount = currents_spikecounts_sorted[rheobase_index - 1]
                            firing_rate = (adjacent_current_spikecount - rheobase_spikecount) / delta_t

                            initial_slope = firing_rate / (adjacent_current - rheobase_current)
                            average_slope = initial_slope

                            self.dataset[cellname]['experiments'][expname]['global_features'][filename]['initial_fI_slope'] = initial_slope
                            self.dataset[cellname]['experiments'][expname]['global_features'][filename]['average_fI_slope'] = average_slope

                            logging.info("Edge case detected in slope feature calculation: rheobase current = {},"
                                         " steady state current = {}, maxspike current = {}".format(rheobase_current,
                                                                                                    steady_state_current,
                                                                                                    highfreq_firing_current))
                        # calculate maximum slope
                        spiking_rate_changes = []
                        for idx, currents_spikecount_tuple in enumerate(currents_spikecounts_sorted):
                            next_idx = idx+1
                            if next_idx == len(currents_spikecounts_sorted):
                                break

                            current, spikecount = currents_spikecount_tuple
                            next_current, next_spikecount = currents_spikecounts_sorted[next_idx]

                            delta_current = next_current - current
                            delta_spikecount = next_spikecount - spikecount
                            spikecount_change = delta_spikecount / delta_current

                            spiking_rate_change = spikecount_change / delta_t
                            spiking_rate_changes.append(spiking_rate_change)
                        self.dataset[cellname]['experiments'][expname]['global_features'][filename]['maximum_fI_slope'] = max(spiking_rate_changes)

                    # calculate baseline current corrected standardized currents
                    if self.correct_standard_currents_with_baseline_current:
                        for current_name in self.standard_currents:
                            if current_dict[current_name]['index'] >= 0:
                                baseline_current = dataset_cell_exp[expname]['baseline_currents'][i_file]
                                current_value = current_dict[current_name]['current']

                                self.dataset[cellname]['experiments'][expname][current_name][filename][
                                    'baseline_corrected_current'] = current_value + baseline_current

                                # print(f"The current for {current_name} was: {current_value}")
                                # print(f"The baseline-corrected current {current_name} is:"
                                #       f"{self.dataset[cellname]['experiments'][expname][current_name][filename]['baseline_corrected_current']}")

    def mean_features(self):
        """Compute the mean for each features for each target"""
        logger.info(" Calculating mean features")

        # mean for each cell
        for i_cell, cellname in enumerate(self.dataset):

            dataset_cell_exp = self.dataset[cellname]['experiments']

            # compute threshold based on some experiments
            if 'expthreshold' in self.options:
                hypamp = []
                amp = []
                numspikes = []

                for i_exp, expname in enumerate(dataset_cell_exp):
                    # use to determine threshold
                    if expname in self.options['expthreshold']:
                        hypamp = hypamp + dataset_cell_exp[expname]['hypamp']
                        amp = amp + dataset_cell_exp[expname]['amp']
                        numspikes = numspikes + dataset_cell_exp[expname][
                            'features']['numspikes']

                mean_hypamp = self.newmeancell(numpy.array(hypamp))
                amp_threshold = self.get_threshold(amp, numspikes)

                self.thresholds_per_cell[cellname] = amp_threshold
                self.hypamps_per_cell[cellname] = mean_hypamp

                logger.info(
                    " %s threshold amplitude: %f hypamp: %f",
                    cellname,
                    amp_threshold,
                    mean_hypamp)

            else:
                self.thresholds_per_cell[cellname] = None
                self.hypamps_per_cell[cellname] = None

            for i_exp, expname in enumerate(dataset_cell_exp):

                # define
                dataset_cell_exp[expname]['mean_amp'] = OrderedDict()
                dataset_cell_exp[expname]['mean_amp_rel'] = OrderedDict()
                dataset_cell_exp[expname]['std_amp'] = OrderedDict()
                dataset_cell_exp[expname]['std_amp_rel'] = OrderedDict()

                dataset_cell_exp[expname]['mean_hypamp'] = OrderedDict()
                dataset_cell_exp[expname]['std_hypamp'] = OrderedDict()

                dataset_cell_exp[expname]['mean_features'] = OrderedDict()
                dataset_cell_exp[expname]['std_features'] = OrderedDict()
                dataset_cell_exp[expname]['n'] = OrderedDict()
                dataset_cell_exp[expname]['raw'] = OrderedDict()

                dataset_cell_exp[expname]['bc_mean_features'] = OrderedDict()
                dataset_cell_exp[expname]['bc_std_features'] = OrderedDict()
                dataset_cell_exp[expname]['bc_shift_features'] = OrderedDict()
                dataset_cell_exp[expname]['bc_ld_features'] = OrderedDict()

                # create mean, std and n fields for global features
                for global_feature in self.global_features:
                    for statistic in ['mean', 'std', 'n']:
                        key = '{}_{}'.format(statistic, global_feature)
                        dataset_cell_exp[expname][key] = OrderedDict()

                # create mean, std, and n fields for rheobase, steady-state and maxspike
                for current_type in self.standard_currents:
                    for statistic in ['mean', 'std', 'n']:
                        key_current = '{}_{}'.format(statistic, current_type)
                        key_features = '{}_{}_features'.format(statistic, current_type)
                        dataset_cell_exp[expname][key_current] = OrderedDict()
                        dataset_cell_exp[expname][key_features] = OrderedDict()

                for feature in self.features[expname]:
                    dataset_cell_exp[expname]['mean_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['std_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['bc_mean_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['bc_std_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['bc_shift_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['bc_ld_features'][feature] = \
                        OrderedDict()
                    dataset_cell_exp[expname]['n'][feature] = OrderedDict()
                    dataset_cell_exp[expname]['raw'][feature] = OrderedDict()

                    # create individual feature fields for each feature inside rheobase, steady-state, maxspike
                    for current_type in self.standard_currents:
                        for statistic in ['mean', 'std', 'n']:
                            key_features = '{}_{}_features'.format(statistic, current_type)
                            dataset_cell_exp[expname][key_features][feature] = OrderedDict()

                ton = dataset_cell_exp[expname]['ton']
                toff = dataset_cell_exp[expname]['toff']
                tend = dataset_cell_exp[expname]['tend']

                ton = self.newmeancell(numpy.array(ton))
                toff = self.newmeancell(numpy.array(toff))
                tend = self.newmeancell(numpy.array(tend))

                hypamp = dataset_cell_exp[expname]['hypamp']
                amp = dataset_cell_exp[expname]['amp']
                numspikes = dataset_cell_exp[expname]['features']['numspikes']
                feature_array = dataset_cell_exp[expname]['features']

                rawfiles_list = dataset_cell_exp[expname]['rawfiles']

                if self.options["relative"]:
                    amp_threshold = self.thresholds_per_cell[cellname]
                    amp_rel = numpy.array(amp / amp_threshold * 100.)
                else:
                    amp_rel = numpy.array(amp)

                # absolute amplitude not relative to hypamp
                amp_abs = numpy.abs(
                    numpy.array(
                        dataset_cell_exp[expname]['amp']) +
                    numpy.array(
                        dataset_cell_exp[expname]['hypamp']))

                i_noinput = numpy.argmin(amp_abs)

                # save amplitude results
                for ti, target in enumerate(self.options["target"]):

                    if target == 'noinput':
                        idx = numpy.array(i_noinput)
                    elif target == 'all':
                        idx = numpy.ones(len(amp), dtype=bool)
                    else:
                        idx = numpy.array(
                            (amp_rel >= (
                                target -
                                self.options["tolerance"][ti])) & (
                                amp_rel <= (
                                    target +
                                    self.options["tolerance"][ti])))

                    amp_target = numpy.atleast_1d(numpy.array(amp)[idx])
                    # equal to amp_target if amplitude not measured relative to
                    # threshold
                    amp_rel_target = numpy.atleast_1d(
                        numpy.array(amp_rel)[idx])
                    hypamp_target = numpy.atleast_1d(numpy.array(hypamp)[idx])

                    if len(amp_target) > 0:

                        if (target == 'noinput'):
                            if (amp_abs[i_noinput] < 0.01):
                                meanamp_target = self.newmeancell(amp_target)
                                stdamp_target = self.newstdcell(amp_target)
                                meanamp_rel_target = self.newmeancell(
                                    amp_rel_target)
                                stdamp_rel_target = self.newstdcell(
                                    amp_rel_target)
                                meanhypamp_target = self.newmeancell(
                                    hypamp_target)
                                stdhypamp_target = self.newstdcell(
                                    hypamp_target)
                            else:
                                continue

                        else:
                            meanamp_target = self.newmeancell(amp_target)
                            stdamp_target = self.newstdcell(amp_target)
                            meanamp_rel_target = self.newmeancell(
                                amp_rel_target)
                            stdamp_rel_target = self.newstdcell(amp_rel_target)
                            meanhypamp_target = self.newmeancell(hypamp_target)
                            stdhypamp_target = self.newstdcell(hypamp_target)

                        dataset_cell_exp[expname]['mean_amp'][
                            str(target)] = meanamp_target
                        dataset_cell_exp[expname]['std_amp'][
                            str(target)] = stdamp_target

                        dataset_cell_exp[expname]['mean_amp_rel'][
                            str(target)] = meanamp_rel_target
                        dataset_cell_exp[expname]['std_amp_rel'][
                            str(target)] = stdamp_rel_target

                        dataset_cell_exp[expname]['mean_hypamp'][
                            str(target)] = meanhypamp_target
                        dataset_cell_exp[expname]['std_hypamp'][
                            str(target)] = stdhypamp_target

                dataset_cell_exp[expname]['mean_ton'] = ton
                dataset_cell_exp[expname]['mean_toff'] = toff
                dataset_cell_exp[expname]['mean_tend'] = tend

                for fi, feature in enumerate(self.features[expname]):
                    feat_vals = numpy.array(feature_array[feature])

                    for ti, target in enumerate(self.options["target"]):

                        if target == 'noinput':
                            idx = numpy.array(i_noinput)
                        elif target == 'all':
                            idx = numpy.ones(len(amp), dtype=bool)
                        else:
                            idx = numpy.array(
                                (amp_rel >= (
                                    target -
                                    self.options["tolerance"][ti])) & (
                                    amp_rel <= (
                                        target +
                                        self.options["tolerance"][ti])))

                        feat = numpy.atleast_1d(numpy.array(feat_vals)[idx])

                        if self.saveraw:
                            raw = numpy.atleast_1d(
                                numpy.array(rawfiles_list)[idx]).tolist()

                        n = numpy.sum(
                            numpy.invert(
                                numpy.isnan(
                                    numpy.atleast_1d(feat))))

                        if n > 0:

                            if (target == 'noinput'):
                                if (amp_abs[i_noinput] < 0.01):
                                    meanfeat = self.newmeancell(feat)
                                    stdfeat = self.newstdcell(feat)
                                    bcmean, bcstd, bcld, bcshift = \
                                        self.boxcoxcell(
                                            feat, nanopt="nanmean_cell")
                                else:
                                    continue
                            else:
                                meanfeat = self.newmeancell(feat)
                                stdfeat = self.newstdcell(feat)
                                bcmean, bcstd, bcld, bcshift = self.boxcoxcell(
                                    feat, nanopt="nanmean_cell")

                            dataset_cell_exp[expname]['mean_features'][
                                feature][
                                str(target)] = meanfeat
                            dataset_cell_exp[expname]['std_features'][
                                feature][
                                str(target)] = stdfeat
                            dataset_cell_exp[expname]['n'][feature][
                                str(target)] = n

                            if self.saveraw:
                                dataset_cell_exp[expname]['raw'][feature][
                                    str(target)] = raw

                            dataset_cell_exp[expname]['bc_mean_features'][
                                feature][
                                str(target)] = bcmean
                            dataset_cell_exp[expname]['bc_std_features'][
                                feature][
                                str(target)] = bcstd
                            dataset_cell_exp[expname]['bc_shift_features'][
                                feature][
                                str(target)] = bcshift
                            dataset_cell_exp[expname]['bc_ld_features'][
                                feature][
                                str(target)] = bcld

                # calculate means and stds for global features (slopes)
                if self.is_global_features_collected:
                    global_feat_single_cell = {}
                    for global_feature in self.global_features:
                        global_feat_single_cell[global_feature] = []

                    for i_file, filename in enumerate(rawfiles_list):
                        for global_feature in self.global_features:
                            if filename in dataset_cell_exp[expname]['global_features']:
                                feature_value = dataset_cell_exp[expname]['global_features'][filename][global_feature]
                                if not numpy.isnan(numpy.atleast_1d(feature_value)):
                                    global_feat_single_cell[global_feature].append(feature_value)

                    for global_feature in self.global_features:
                        feature_values = global_feat_single_cell[global_feature]
                        n = len(feature_values)
                        if n > 0:
                            key_mean = 'mean_{globalfeat}'.format(globalfeat=global_feature)
                            key_std = 'std_{globalfeat}'.format(globalfeat=global_feature)
                            key_n = 'n_{globalfeat}'.format(globalfeat=global_feature)
                            dataset_cell_exp[expname][key_mean] = self.newmeancell(feature_values)
                            dataset_cell_exp[expname][key_std] = self.newstdcell(feature_values)
                            dataset_cell_exp[expname][key_n] = n

                    # calculate means and stds for standard currents and their corresponding features
                    standard_currents_single_cell = {}
                    for current_type in self.standard_currents:
                        standard_currents_single_cell[current_type] = {
                            'currents': [],
                            'features': defaultdict(list)
                        }
                        if self.correct_standard_currents_with_baseline_current:
                            standard_currents_single_cell[current_type]['baseline_corrected_currents'] = []

                    for i_file, filename in enumerate(rawfiles_list):
                        for current_type in standard_currents_single_cell:
                            if 'current' in dataset_cell_exp[expname][current_type][filename]:
                                current = dataset_cell_exp[expname][current_type][filename]['current']
                                if not numpy.isnan(numpy.atleast_1d(current)):
                                    standard_currents_single_cell[current_type]['currents'].append(current)
                                for feature, feature_value in dataset_cell_exp[expname][current_type][filename]['features'].items():
                                    if not numpy.isnan(numpy.atleast_1d(feature_value)):
                                        standard_currents_single_cell[current_type]['features'][feature].append(feature_value)
                                if self.correct_standard_currents_with_baseline_current:
                                    baseline_corrected_current = self.dataset[cellname]['experiments'][expname][current_type][filename]['baseline_corrected_current']
                                    standard_currents_single_cell[current_type]['baseline_corrected_currents'].append(baseline_corrected_current)

                    for current_type in standard_currents_single_cell:
                        currents = standard_currents_single_cell[current_type]['currents']
                        features = standard_currents_single_cell[current_type]['features']
                        n_currents = len(currents)
                        if n_currents > 0:
                            key_mean = 'mean_{current}'.format(current=current_type)
                            key_std = 'std_{current}'.format(current=current_type)
                            key_n = 'n_{current}'.format(current=current_type)
                            key_mean_feat = '{key_mean}_features'.format(key_mean=key_mean)
                            key_std_feat = '{key_std}_features'.format(key_std=key_std)
                            key_n_feat = '{key_n}_features'.format(key_n=key_n)

                            dataset_cell_exp[expname][key_mean] = self.newmeancell(currents)
                            dataset_cell_exp[expname][key_std] = self.newstdcell(currents)
                            dataset_cell_exp[expname][key_n] = n_currents
                            for feature in features:
                                n_features = len(features[feature])
                                if n_features > 0:
                                    dataset_cell_exp[expname][key_mean_feat][feature] = self.newmeancell(features[feature])
                                    dataset_cell_exp[expname][key_std_feat][feature] = self.newstdcell(features[feature])
                                    dataset_cell_exp[expname][key_n_feat][feature] = n_features

                        if self.correct_standard_currents_with_baseline_current:
                            baseline_corrected_currents = standard_currents_single_cell[current_type]['baseline_corrected_currents']
                            if n_currents > 0:
                                key_mean = 'mean_{current}'.format(current=current_type + '_baseline_corrected')
                                key_std = 'std_{current}'.format(current=current_type + '_baseline_corrected')
                                key_n = 'n_{current}'.format(current=current_type + '_baseline_corrected')
                                dataset_cell_exp[expname][key_mean] = self.newmeancell(baseline_corrected_currents)
                                dataset_cell_exp[expname][key_std] = self.newstdcell(baseline_corrected_currents)
                                dataset_cell_exp[expname][key_n] = n_currents
                            if n_currents != len(baseline_corrected_currents):
                                print("Something is wrong: n_currents != len(baseline_corrected_currents)")

        # mean for all cells
        for i_exp, expname in enumerate(self.experiments):

            # collect everything in global structure
            self.dataset_mean[expname] = OrderedDict()
            self.dataset_mean[expname]['amp'] = OrderedDict()
            self.dataset_mean[expname]['amp_rel'] = OrderedDict()
            self.dataset_mean[expname]['hypamp'] = OrderedDict()
            self.dataset_mean[expname]['ton'] = []
            self.dataset_mean[expname]['toff'] = []
            self.dataset_mean[expname]['tend'] = []
            self.dataset_mean[expname]['features'] = OrderedDict()
            self.dataset_mean[expname]['cell_std_features'] = OrderedDict()
            self.dataset_mean[expname]['cell_bc_features'] = OrderedDict()
            self.dataset_mean[expname]['cell_n'] = OrderedDict()
            self.dataset_mean[expname]['n'] = OrderedDict()
            self.dataset_mean[expname]['raw'] = OrderedDict()

            # create mean, std and n fields for global features
            for global_feature in self.global_features:
                for statistic in ['mean', 'std', 'n']:
                    key = '{}_{}'.format(statistic, global_feature)
                    self.dataset_mean[expname][key] = OrderedDict()

            # create mean, std, and n fields for rheobase, steady-state and maxspike
            for current_type in self.standard_currents:
                for statistic in ['mean', 'std', 'n']:
                    key_current = '{}_{}'.format(statistic, current_type)
                    key_features = '{}_{}_features'.format(statistic, current_type)
                    self.dataset_mean[expname][key_current] = OrderedDict()
                    self.dataset_mean[expname][key_features] = OrderedDict()
                    if self.correct_standard_currents_with_baseline_current:
                        key_corrected_current = '{}_{}'.format(statistic, current_type + '_baseline_corrected')
                        self.dataset_mean[expname][key_corrected_current] = OrderedDict()

            for feature in self.features[expname]:
                self.dataset_mean[expname]['features'][feature] = OrderedDict()
                self.dataset_mean[expname]['cell_std_features'][feature] = \
                    OrderedDict()
                self.dataset_mean[expname]['cell_bc_features'][feature] = \
                    OrderedDict()
                self.dataset_mean[expname]['cell_n'][feature] = OrderedDict()
                self.dataset_mean[expname]['n'][feature] = OrderedDict()
                self.dataset_mean[expname]['raw'][feature] = OrderedDict()

                # create individual feature fields for each feature inside rheobase, steady-state, maxspike
                for current_type in self.standard_currents:
                    for statistic in ['mean', 'std', 'n']:
                        key_features = '{}_{}_features'.format(statistic, current_type)
                        self.dataset_mean[expname][key_features][feature] = OrderedDict()

                for target in self.options["target"]:
                    self.dataset_mean[expname]['features'][feature][
                        str(target)] = []
                    self.dataset_mean[expname][
                        'cell_std_features'][feature][str(target)] = []
                    self.dataset_mean[expname][
                        'cell_bc_features'][feature][str(target)] = []
                    self.dataset_mean[expname]['cell_n'][feature][
                        str(target)] = []
                    self.dataset_mean[expname]['n'][feature][str(target)] = []
                    self.dataset_mean[expname]['raw'][feature][
                        str(target)] = []

            for target in self.options["target"]:
                self.dataset_mean[expname]['amp'][str(target)] = []
                self.dataset_mean[expname]['amp_rel'][str(target)] = []
                self.dataset_mean[expname]['hypamp'][str(target)] = []

            standard_currents_all_cells = {}
            global_feat_all_cells = {}
            for current_type in self.standard_currents:
                standard_currents_all_cells[current_type] = {
                    'currents': [],
                    'features': defaultdict(list),
                    'features_exist': defaultdict(bool),  # when features are gathered file by file, if a feature existed in any measurement, this will turn true for that feature (this is used later for counting how many cells had a given feature)
                    'cell_n_currents': 0,
                    'cell_n_features': defaultdict(int)
                }
                if self.correct_standard_currents_with_baseline_current:
                    standard_currents_all_cells[current_type]['baseline_corrected_currents'] = []
            for global_feat in self.global_features:
                global_feat_all_cells[global_feat] = {
                    'feat_vals': [],
                    'cell_n': 0
                }

            for i_cell, cellname in enumerate(self.dataset):

                dataset_cell_exp = self.dataset[cellname]['experiments']
                rawfiles_list = dataset_cell_exp[expname]['rawfiles']

                if expname in dataset_cell_exp:
                    self.dataset_mean[expname]['location'] =\
                        dataset_cell_exp[expname]['location']

                    ton = dataset_cell_exp[expname]['mean_ton']
                    self.dataset_mean[expname]['ton'].append(ton)

                    toff = dataset_cell_exp[expname]['mean_toff']
                    self.dataset_mean[expname]['toff'].append(toff)

                    tend = dataset_cell_exp[expname]['mean_tend']
                    self.dataset_mean[expname]['tend'].append(tend)

                    for target in self.options["target"]:
                        if str(target) in dataset_cell_exp[expname][
                                'mean_amp']:
                            amp = dataset_cell_exp[expname]['mean_amp'][
                                str(target)]
                            self.dataset_mean[expname]['amp'][
                                str(target)].append(amp)
                            amp_rel = dataset_cell_exp[expname][
                                'mean_amp_rel'][
                                str(target)]
                            self.dataset_mean[expname]['amp_rel'][
                                str(target)].append(amp_rel)
                            hypamp = dataset_cell_exp[expname][
                                'mean_hypamp'][str(target)]
                            self.dataset_mean[expname]['hypamp'][
                                str(target)].append(hypamp)

                    for feature in self.features[expname]:
                        for target in self.options["target"]:
                            if str(target) in dataset_cell_exp[expname][
                                    'mean_features'][feature]:

                                result = dataset_cell_exp[expname][
                                    'mean_features'][feature][
                                    str(target)]
                                self.dataset_mean[expname]['features'][
                                    feature][str(target)].append(result)

                                cell_std_result = dataset_cell_exp[expname][
                                    'std_features'][feature][str(target)]
                                self.dataset_mean[expname][
                                    'cell_std_features'][feature][
                                    str(target)].append(cell_std_result)

                                bcmean = dataset_cell_exp[expname][
                                    'bc_mean_features'][feature][
                                    str(target)]
                                bcstd = dataset_cell_exp[expname][
                                    'bc_std_features'][feature][
                                    str(target)]
                                bcshift = dataset_cell_exp[expname][
                                    'bc_shift_features'][feature][
                                    str(target)]
                                bcld = dataset_cell_exp[expname][
                                    'bc_ld_features'][feature][
                                    str(target)]
                                self.dataset_mean[expname][
                                    'cell_bc_features'][feature][str(
                                        target)].append(
                                    [bcmean, bcstd, bcld, bcshift])

                                n = dataset_cell_exp[expname]['n'][feature][
                                    str(target)]
                                self.dataset_mean[expname][
                                    'cell_n'][feature][
                                    str(target)].append(n)

                                if self.saveraw:
                                    raw = dataset_cell_exp[expname]['raw'][
                                        feature][
                                        str(target)]
                                    self.dataset_mean[expname]['raw'][
                                        feature][
                                        str(target)].append(raw)

                    # set up a file counter for standard currents and global features
                    if self.is_global_features_collected:
                        file_nums = {}
                        for element in self.standard_currents + self.global_features:
                            file_nums[element] = 0

                        # count files with valid currents and global features, concatenate values from different files
                        for current_type in standard_currents_all_cells:
                            for feature in self.features[expname]:
                                standard_currents_all_cells[current_type]['features_exist'][feature] = False
                                ''' trying to debug'''
                                '''
                                if feature == "AHP_depth_abs_slow" and current_type == "rheobase_current":
                                    print(f"setup: {cellname}, {current_type}, {feature}, {standard_currents_all_cells[current_type]['features_exist'][feature]}")
                                '''
                                ''' trying to debug end'''
                        for i_file, filename in enumerate(rawfiles_list):
                            for current_type in standard_currents_all_cells:
                                ''' SS '''
                                for feature in self.features[expname]:
                                    standard_currents_all_cells[current_type]['features_exist'][feature] = False
                                ''' SS '''
                                if 'current' in dataset_cell_exp[expname][current_type][filename]:
                                    current = dataset_cell_exp[expname][current_type][filename]['current']
                                    if not numpy.isnan(numpy.atleast_1d(current)):
                                        standard_currents_all_cells[current_type]['currents'].append(current)
                                        file_nums[current_type] += 1
                                    for feature, feature_value in dataset_cell_exp[expname][current_type][filename]['features'].items():
                                        if feature not in self.features[expname]:
                                            continue
                                        if not numpy.isnan(numpy.atleast_1d(feature_value)):
                                            standard_currents_all_cells[current_type]['features'][feature].append(feature_value)
                                            standard_currents_all_cells[current_type]['features_exist'][feature] = True   ### ezt minden file-nal ujra atirja a szerint, h abban epp nan-e az adott feature, ahhoz, h ez hasznalhato legyen kesobb, fajlonkent kene elmenteni
                                            ''' trying to debug'''
                                            '''
                                            if feature == "AHP_depth_abs_slow" and current_type == "rheobase_current":
                                                print(f"exists: {cellname}, {current_type}, {feature}, {standard_currents_all_cells[current_type]['features_exist'][feature]}, {feature_value}")
                                            '''
                                            ''' trying to debug end'''
                                    if self.correct_standard_currents_with_baseline_current:
                                        baseline_corrected_current = dataset_cell_exp[expname][current_type][filename]['baseline_corrected_current']
                                        standard_currents_all_cells[current_type]['baseline_corrected_currents'].append(baseline_corrected_current)

                            if filename not in dataset_cell_exp[expname]['global_features']:
                                continue
                            for global_feature_type in global_feat_all_cells:
                                if global_feature_type in dataset_cell_exp[expname]['global_features'][filename]:
                                    global_feature_value = dataset_cell_exp[expname]['global_features'][filename][global_feature_type]
                                    if not numpy.isnan(numpy.atleast_1d(global_feature_value)):
                                        global_feat_all_cells[global_feature_type]['feat_vals'].append(global_feature_value)
                                        file_nums[global_feature_type] += 1

                        for current_type in standard_currents_all_cells:
                            if file_nums[current_type] > 0:
                                standard_currents_all_cells[current_type]['cell_n_currents'] += 1
                                for feature in standard_currents_all_cells[current_type]['features']:
                                    ''' trying to debug'''
                                    '''
                                    if current_type == 'rheobase_current' and feature == 'AHP_depth_abs_slow':
                                        #print(cellname, standard_currents_all_cells[current_type]['features'][feature])
                                        with open("cells_AHP_depth_abs_slow.txt", "a") as f:
                                            f.writelines([cellname, ": ", str(standard_currents_all_cells[current_type]['features'][feature]), "\n"])
                                    '''
                                    ''' trying to debug end'''
                                    '''
                                    if standard_currents_all_cells[current_type]['features_exist'][feature]:
                                        standard_currents_all_cells[current_type]['cell_n_features'][feature] += 1
                                    '''
                                    standard_currents_all_cells[current_type]['cell_n_features'][feature] = len(standard_currents_all_cells[current_type]['features'][feature])  # added by SS - works because in line 1341 only not NaN values are appended to this list
                        for global_feature_type in global_feat_all_cells:
                            if file_nums[global_feature_type] > 0:
                                global_feat_all_cells[global_feature_type]['cell_n'] += 1

            # create means
            self.dataset_mean[expname]['mean_amp'] = OrderedDict()
            self.dataset_mean[expname]['mean_amp_rel'] = OrderedDict()
            self.dataset_mean[expname]['mean_hypamp'] = OrderedDict()
            self.dataset_mean[expname]['std_amp'] = OrderedDict()
            self.dataset_mean[expname]['std_amp_rel'] = OrderedDict()
            self.dataset_mean[expname]['std_hypamp'] = OrderedDict()
            self.dataset_mean[expname]['mean_features'] = OrderedDict()
            self.dataset_mean[expname]['std_features'] = OrderedDict()

            self.dataset_mean[expname]['bc_mean_features'] = OrderedDict()
            self.dataset_mean[expname]['bc_std_features'] = OrderedDict()
            self.dataset_mean[expname]['bc_shift_features'] = OrderedDict()
            self.dataset_mean[expname]['bc_ld_features'] = OrderedDict()

            for feature in self.features[expname]:
                self.dataset_mean[expname][
                    'mean_features'][feature] = OrderedDict()
                self.dataset_mean[expname][
                    'std_features'][feature] = OrderedDict()

                self.dataset_mean[expname][
                    'bc_mean_features'][feature] = OrderedDict()
                self.dataset_mean[expname][
                    'bc_std_features'][feature] = OrderedDict()
                self.dataset_mean[expname][
                    'bc_shift_features'][feature] = OrderedDict()
                self.dataset_mean[expname][
                    'bc_ld_features'][feature] = OrderedDict()

            ton = self.dataset_mean[expname]['ton']
            toff = self.dataset_mean[expname]['toff']
            tend = self.dataset_mean[expname]['tend']

            self.dataset_mean[expname]['mean_ton'] = self.newmean(ton)
            self.dataset_mean[expname]['mean_toff'] = self.newmean(toff)
            self.dataset_mean[expname]['mean_tend'] = self.newmean(tend)

            for target in self.options["target"]:
                amp = self.dataset_mean[expname]['amp'][str(target)]
                amp_rel = self.dataset_mean[expname]['amp_rel'][str(target)]
                hypamp = self.dataset_mean[expname]['hypamp'][str(target)]

                self.dataset_mean[expname]['mean_amp'][
                    str(target)] = self.newmean(amp)
                self.dataset_mean[expname]['mean_amp_rel'][
                    str(target)] = self.newmean(amp_rel)
                self.dataset_mean[expname]['mean_hypamp'][
                    str(target)] = self.newmean(hypamp)
                self.dataset_mean[expname]['std_amp'][
                    str(target)] = self.newstd(amp)
                self.dataset_mean[expname]['std_amp_rel'][
                    str(target)] = self.newstd(amp_rel)
                self.dataset_mean[expname]['std_hypamp'][
                    str(target)] = self.newstd(hypamp)

            for feature in self.features[expname]:
                for target in self.options["target"]:
                    feat = self.dataset_mean[expname]['features'][feature][
                        str(target)]
                    cell_std_feat = self.dataset_mean[expname][
                        'cell_std_features'][feature][str(target)]
                    cell_n = self.dataset_mean[expname]['cell_n'][feature][
                        str(target)]

                    # added by Luca Leonardo Bologna to handle the case in
                    # which only one feature value is present at this point
                    # count nonNan entries!

                    n = numpy.sum(
                        numpy.invert(
                            numpy.isnan(
                                numpy.atleast_1d(feat))))
                    self.dataset_mean[expname]['n'][feature][str(target)] = n

                    if n == 1:  # only result from one cell in population
                        # pick values from this cell
                        val_idx = numpy.where(~numpy.isnan(
                            numpy.atleast_1d(feat)))[0][0]
                        self.dataset_mean[expname]['mean_features'][
                            feature][str(target)] = feat[val_idx]
                        self.dataset_mean[expname]['std_features'][
                            feature][str(target)] = cell_std_feat[val_idx]
                        [bcmean, bcstd, bcld, bcshift] = \
                            self.dataset_mean[expname][
                            'cell_bc_features'][feature][str(
                                target)][val_idx]
                    else:
                        self.dataset_mean[expname][
                            'mean_features'][feature][str(
                                target)] = self.newmean(feat)
                        self.dataset_mean[expname]['std_features'][feature][
                            str(target)] = self.newstd(feat)
                        bcmean, bcstd, bcld, bcshift = self.boxcoxcell(
                            feat, nanopt="nanmean")

                    self.dataset_mean[expname]['bc_mean_features'][feature][
                        str(target)] = bcmean
                    self.dataset_mean[expname]['bc_std_features'][feature][
                        str(target)] = bcstd
                    self.dataset_mean[expname][
                        'bc_shift_features'][feature][str(
                            target)] = bcshift
                    self.dataset_mean[expname]['bc_ld_features'][feature][
                        str(target)] = bcld

            # calculate means, stds for standard currents
            if self.is_global_features_collected:
                for current_type in standard_currents_all_cells:
                    currents = standard_currents_all_cells[current_type]['currents']
                    features = standard_currents_all_cells[current_type]['features']
                    n_currents = standard_currents_all_cells[current_type]['cell_n_currents']
                    if n_currents > 0:
                        key_mean = 'mean_{current}'.format(current=current_type)
                        key_std = 'std_{current}'.format(current=current_type)
                        key_n = 'n_{current}'.format(current=current_type)
                        key_mean_feat = '{key_mean}_features'.format(key_mean=key_mean)
                        key_std_feat = '{key_std}_features'.format(key_std=key_std)
                        key_n_feat = '{key_n}_features'.format(key_n=key_n)

                        self.dataset_mean[expname][key_mean] = self.newmeancell(currents)
                        self.dataset_mean[expname][key_std] = self.newstdcell(currents)
                        self.dataset_mean[expname][key_n] = n_currents
                        for feature in features:
                            n_features = standard_currents_all_cells[current_type]['cell_n_features'][feature]
                            if n_features > 0:
                                self.dataset_mean[expname][key_mean_feat][feature] = self.newmeancell(features[feature])
                                self.dataset_mean[expname][key_std_feat][feature] = self.newstdcell(features[feature])
                                self.dataset_mean[expname][key_n_feat][feature] = n_features

                    if self.correct_standard_currents_with_baseline_current:
                        baseline_corrected_currents = standard_currents_all_cells[current_type]['baseline_corrected_currents']
                        if n_currents > 0:
                            key_mean = 'mean_{current}'.format(current=current_type + '_baseline_corrected')
                            key_std = 'std_{current}'.format(current=current_type + '_baseline_corrected')
                            key_n = 'n_{current}'.format(current=current_type + '_baseline_corrected')
                            self.dataset_mean[expname][key_mean] = self.newmeancell(baseline_corrected_currents)
                            self.dataset_mean[expname][key_std] = self.newstdcell(baseline_corrected_currents)
                            self.dataset_mean[expname][key_n] = n_currents
                            # print("current_type", current_type)
                            # print("baseline_corrected_currents", baseline_corrected_currents)
                        if len(currents) != len(baseline_corrected_currents):
                            print("Something is wrong: n_currents != len(baseline_corrected_currents) for all cells "
                                  f"{n_currents} != {len(baseline_corrected_currents)}")

            # calculate means, stds for global features
            for global_feature in global_feat_all_cells:
                feature_values = global_feat_all_cells[global_feature]['feat_vals']
                n_globalfeat = global_feat_all_cells[global_feature]['cell_n']
                if n_globalfeat > 0:
                    key_mean = 'mean_{globalfeat}'.format(globalfeat=global_feature)
                    key_std = 'std_{globalfeat}'.format(globalfeat=global_feature)
                    key_n = 'n_{globalfeat}'.format(globalfeat=global_feature)
                    self.dataset_mean[expname][key_mean] = self.newmeancell(feature_values)
                    self.dataset_mean[expname][key_std] = self.newstdcell(feature_values)
                    self.dataset_mean[expname][key_n] = n_globalfeat

    def get_threshold(self, amp, numspikes):
        """Get the spiking threshold of a cell by taking the smallest current
        amplitude for which it fires"""
        isort = numpy.argsort(amp)
        amps_sort = numpy.array(amp)[isort]
        numspikes_sort = numpy.array(numspikes)[isort]
        i_threshold = numpy.where(
            numspikes_sort >= self.options["spike_threshold"])[0][0]
        amp_threshold = amps_sort[i_threshold]

        return amp_threshold

    def plt_features(self):
        """Plot the features"""
        logger.info(" Plotting features")
        figs = OrderedDict()

        markercyclercell = cycle(self.markerlist)
        colorcyclercell = cycle(self.colorlist)

        for i_cell, cellname in enumerate(self.dataset):

            cellfigs = OrderedDict()

            dirname = self.maindirname + cellname
            tools.makedir(dirname)

            colorcell = next(colorcyclercell)
            markercell = next(markercyclercell)
            dataset_cell_exp = self.dataset[cellname]['experiments']

            for i_exp, expname in enumerate(dataset_cell_exp):

                figname = "features_" + expname
                if figname not in figs:
                    plottools.tiled_figure(
                        figname, frames=len(self.features[expname]),
                        columns=3, figs=figs, dirname=self.maindirname,
                        top=0.97, bottom=0.04, left=0.07, right=0.97,
                        hspace=0.75, wspace=0.3)

                figname = "features_" + cellname.split('/')[-1] + "_" + expname
                axs_cell = plottools.tiled_figure(
                    figname,
                    frames=len(
                        self.features[expname]),
                    columns=3,
                    figs=cellfigs,
                    dirname=dirname,
                    top=0.97,
                    bottom=0.04,
                    left=0.07,
                    right=0.97,
                    hspace=0.75,
                    wspace=0.3)

                amp = dataset_cell_exp[expname]['amp']
                feature_array = dataset_cell_exp[expname]['features']
                filenames = dataset_cell_exp[expname]['filename']

                markercycler = cycle(self.markerlist)
                colorcycler = cycle(self.colorlist)

                colormarker_dict = {u: [next(colorcycler), next(
                    markercycler)] for u in list(set(filenames))}

                if self.options["relative"]:
                    amp_threshold = self.thresholds_per_cell[cellname]
                    amp_rel = amp / amp_threshold * 100.
                else:
                    amp_rel = amp

                for fi, feature in enumerate(self.features[expname]):

                    feat_vals = numpy.array(feature_array[feature])

                    for i_feat, feat_vals_ in enumerate(feat_vals):
                        color = colormarker_dict[filenames[i_feat]][0]
                        marker = colormarker_dict[filenames[i_feat]][1]

                        amp_rel_ = numpy.float64(amp_rel[i_feat])
                        is_not_nan = ~numpy.isnan(feat_vals_)

                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            axs_cell[fi].plot(
                                amp_rel_[is_not_nan],
                                feat_vals_[is_not_nan],
                                "",
                                linestyle='None',
                                marker=marker,
                                color=color,
                                markersize=5,
                                zorder=1,
                                linewidth=1,
                                markeredgecolor='none',
                                clip_on=False)
                        # axs_cell[fi].set_xticks(self.options["target"])
                        # axs_cell[fi].set_xticklabels(())
                        axs_cell[fi].set_title(feature)

                        figname = "features_" + expname
                        with warnings.catch_warnings():
                            warnings.simplefilter('ignore')
                            figs[figname]['axs'][fi].plot(
                                amp_rel_[is_not_nan],
                                feat_vals_[is_not_nan],
                                "", linestyle='None', marker=markercell,
                                color=colorcell, markersize=3, zorder=1,
                                linewidth=1, markeredgecolor='none', clip_on=False)
                        figs[figname]['axs'][fi].set_title(feature)

                    if 'mean_features' in dataset_cell_exp[expname]:

                        amp_rel_list = []
                        mean_list = []
                        std_list = []
                        for target in self.options["target"]:
                            if str(target) in dataset_cell_exp[expname][
                                    'mean_features'][feature]:
                                a = dataset_cell_exp[expname][
                                    'mean_amp_rel'][str(
                                        target)]
                                m = dataset_cell_exp[expname][
                                    'mean_features'][feature][str(
                                        target)]
                                s = dataset_cell_exp[expname][
                                    'std_features'][feature][str(
                                        target)]

                                if "zero_std" in self.options and \
                                        self.options["zero_std"]:
                                    rules = [~numpy.isnan(m)]
                                else:
                                    rules = [
                                        ~numpy.isnan(m), (s > 0.0) or
                                        (m == 0.0)]
                                if all(rules):
                                    amp_rel_list.append(a)
                                    mean_list.append(m)
                                    std_list.append(s)

                        mean_array = numpy.array(mean_list)
                        std_array = numpy.array(std_list)
                        amp_rel_array = numpy.array(amp_rel_list)

                        e = axs_cell[fi].errorbar(
                            amp_rel_array, mean_array, yerr=std_array,
                            marker='s', color='k', linewidth=1,
                            linestyle='None', markersize=6, zorder=10,
                            clip_on=False)
                        # axs_cell[fi].set_xticks(self.options["target"])
                        for b in e[1]:
                            b.set_clip_on(False)

            # close single cell figures
            for i_fig, figname in enumerate(cellfigs):
                fig = cellfigs[figname]
                fig['fig'].savefig(
                    fig['dirname'] + '/' + figname + '.pdf', dpi=300)
                plt.close(fig['fig'])

        for i_exp, expname in enumerate(self.experiments):

            if expname in self.dataset_mean:
                for fi, feature in enumerate(self.features[expname]):
                    amp_rel_list = []
                    mean_list = []
                    std_list = []
                    for target in self.options["target"]:
                        if str(target) in self.dataset_mean[expname][
                                'mean_features'][feature]:
                            a = self.dataset_mean[expname]['mean_amp_rel'][
                                str(target)]
                            m = self.dataset_mean[expname]['mean_features'][
                                feature][
                                str(target)]
                            s = self.dataset_mean[expname]['std_features'][
                                feature][
                                str(target)]

                            if "zero_std" in self.options and \
                                    self.options["zero_std"]:
                                rules = [~numpy.isnan(m)]
                            else:
                                rules = [
                                    ~numpy.isnan(m), (s > 0.0) or
                                    (m == 0.0)]
                            if all(rules):
                                amp_rel_list.append(a)
                                mean_list.append(m)
                                std_list.append(s)

                    mean_array = numpy.array(mean_list)
                    std_array = numpy.array(std_list)
                    amp_rel_array = numpy.array(amp_rel_list)

                    figname = "features_" + expname
                    e = figs[figname]['axs'][fi].errorbar(
                        amp_rel_list, mean_array, yerr=std_array, marker='s',
                        color='k', linewidth=1, linestyle='None', markersize=6,
                        zorder=10, clip_on=False)
                    for b in e[1]:
                        b.set_clip_on(False)

        for i_fig, figname in enumerate(figs):
            fig = figs[figname]
            fig['fig'].savefig(
                fig['dirname'] +
                '/' +
                figname +
                '.pdf',
                dpi=300)
            plt.close(fig['fig'])

    def plt_features_dist(self):
        """Plot the distribution of features"""
        logger.info(" Plotting feature distributions")
        figs = OrderedDict()

        dirname = self.maindirname + 'dists'
        tools.makedir(dirname)

        for i_exp, expname in enumerate(self.experiments):

            figpath = dirname + '/features_' + expname + '.pdf'
            pdf_pages = PdfPages(figpath)

            for feature in self.features[expname]:

                figname = "features_" + expname + "_" + feature
                axs = plottools.tiled_figure(
                    figname, frames=2 * len(self.options["target"]),
                    columns=6, figs=figs, dirname=dirname, top=0.92,
                    bottom=0.04, left=0.07, right=0.97, hspace=0.75,
                    wspace=0.3)

                for it, target in enumerate(self.options["target"]):

                    feat = numpy.array(
                        self.dataset_mean[expname]['features'][feature]
                        [str(target)])

                    ax = axs[2 * it]
                    ax_bc = axs[2 * it + 1]
                    ax.set_title(str(target))
                    ax_bc.set_title(str(target) + " boxcox")
                    feat[numpy.isinf(feat)] = float('nan')

                    bcshift = \
                        self.dataset_mean[expname][
                            'bc_shift_features'][feature][str(
                                target)]
                    bcld = self.dataset_mean[expname]['bc_ld_features'][
                        feature][
                        str(target)]

                    # removing nan values before plotting
                    feat = feat[numpy.logical_not(numpy.isnan(feat))]
                    if (all(numpy.isnan(feat)) is False):

                        ax.hist(feat, max(1, int(len(feat) / 2)),
                                histtype='stepfilled', color='b',
                                edgecolor='none')
                        ax_bc.set_title(
                            str(target) +
                            " boxcox\nld:" +
                            str(bcld) +
                            "\nshift:" +
                            str(bcshift))

                fig = figs[figname]
                fig['fig'].suptitle(feature)
                pdf_pages.savefig(fig['fig'])

            pdf_pages.close()

    def feature_config_all(self, version=None):
        self.create_feature_config(self.maindirname,
                                   self.dataset_mean, version=version)

    def feature_config_cells(self, version=None):
        for i_cell, cellname in enumerate(self.dataset):
            dirname = self.maindirname + cellname
            tools.makedir(dirname)
            dataset_cell_exp = self.dataset[cellname]['experiments']
            self.create_feature_config(self.maindirname + cellname + os.sep,
                                       dataset_cell_exp, version=version)

    def feature_config_meas(self, version=None):
        for i_cell, cellname in enumerate(self.dataset):
            for i_exp, expname in enumerate(self.dataset[cellname]['experiments']):
                dataset_cell_exp = self.dataset[cellname]['experiments'][expname]
                measurement_files = self.config['cells'][cellname]['experiments'][expname]['files']  # list of unique files

                for unique_measurement_file in measurement_files:
                    # create single-measurement-file dataset slice
                    dataset_cell_exp_slice = OrderedDict()
                    dataset_cell_exp_slice[expname] = OrderedDict()
                    dataset_cell_exp_slice[expname]['location'] = dataset_cell_exp['location']
                    dataset_components = ["voltage", "current", "dt", "filename", "t", "ton", "tend", "toff", "amp", "hypamp", "files"]
                    for dataset_component in dataset_components:
                        dataset_cell_exp_slice[expname][dataset_component] = []
                    dataset_cell_exp_slice[expname]["rawfiles"] = [unique_measurement_file]
                    dataset_cell_exp_slice[expname]["features"] = OrderedDict()

                    # fill up dataset slice
                    for idx, current_measurement_file in enumerate(dataset_cell_exp["filename"]):
                        if unique_measurement_file == current_measurement_file:
                            # copy non-feature values from original cell belonging to a given meas file
                            for dataset_component in dataset_components:
                                if dataset_cell_exp[dataset_component]:
                                    dataset_cell_exp_slice[expname][dataset_component].append(dataset_cell_exp[dataset_component][idx])

                            # copy features from original cell belonging to a given meas file
                            for feature in dataset_cell_exp["features"]:
                                if feature not in dataset_cell_exp_slice[expname]["features"]:
                                    dataset_cell_exp_slice[expname]["features"][feature] = []
                                dataset_cell_exp_slice[expname]["features"][feature].append(dataset_cell_exp["features"][feature][idx])

                    # copy feature values to "mean" feature values (since this time it is a mean over 1 measurement)
                    dataset_cell_exp_slice[expname]["mean_features"] = dataset_cell_exp_slice[expname]["features"]
                    dataset_cell_exp_slice[expname]["std_features"] = dataset_cell_exp_slice[expname]["features"]
                    dataset_cell_exp_slice[expname]["global_features"] = {}
                    try:
                        dataset_cell_exp_slice[expname]["global_features"][unique_measurement_file] = dataset_cell_exp["global_features"][unique_measurement_file]
                        for standard_current in self.standard_currents:
                            dataset_cell_exp_slice[expname][standard_current] = defaultdict(dict)
                            dataset_cell_exp_slice[expname][standard_current][unique_measurement_file] = dataset_cell_exp[standard_current][unique_measurement_file]
                        for feat in self.global_features:
                            dataset_cell_exp_slice[expname]["mean_{}".format(feat)] = dataset_cell_exp_slice[expname]["global_features"][unique_measurement_file][feat]
                            dataset_cell_exp_slice[expname]["std_{}".format(feat)] = 0.01
                            dataset_cell_exp_slice[expname]["n_{}".format(feat)] = 1
                        for curr in self.standard_currents:
                            dataset_cell_exp_slice[expname]["mean_{}".format(curr)] = dataset_cell_exp_slice[expname][curr][unique_measurement_file]['current']
                            dataset_cell_exp_slice[expname]["std_{}".format(curr)] = 0.01
                            dataset_cell_exp_slice[expname]["n_{}".format(curr)] = 1
                            dataset_cell_exp_slice[expname]["mean_{}_features".format(curr)] = dataset_cell_exp_slice[expname][curr][unique_measurement_file]['features']
                            dataset_cell_exp_slice[expname]["std_{}_features".format(curr)] = OrderedDict()
                            dataset_cell_exp_slice[expname]["n_{}_features".format(curr)] = OrderedDict()
                            for feat in dataset_cell_exp_slice[expname]["mean_{}_features".format(curr)]:
                                dataset_cell_exp_slice[expname]["std_{}_features".format(curr)][feat] = 0.01
                                dataset_cell_exp_slice[expname]["n_{}_features".format(curr)][feat] = 1
                            if self.correct_standard_currents_with_baseline_current:
                                dataset_cell_exp_slice[expname]["mean_{}".format(curr + '_baseline_corrected')] = \
                                dataset_cell_exp_slice[expname][curr][unique_measurement_file]['baseline_corrected_current']
                                dataset_cell_exp_slice[expname]["std_{}".format(curr + '_baseline_corrected')] = 0.01
                                dataset_cell_exp_slice[expname]["n_{}".format(curr + '_baseline_corrected')] = 1

                        output_path = self.maindirname + cellname + os.sep + unique_measurement_file + os.sep
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        self.create_feature_config(output_path, dataset_cell_exp_slice, version=version)
                    except KeyError as e:
                        logging.exception(e)
                        continue

    def analyse_threshold(self):
        """Get the spiking threshold and holding current for  all cells. Save
        them in hypamp_threshold.json"""
        logger.info(
            " Analysing threshold and hypamp and saving files to %s",
            self.maindirname)

        hyp_th = {}
        for cellname in self.thresholds_per_cell:
            hyp_th[cellname] = OrderedDict()
            hyp_th[cellname]['threshold'] = round(
                self.thresholds_per_cell[cellname], 4)
            hyp_th[cellname]['hypamp'] = round(
                self.hypamps_per_cell[cellname], 4)

        thresholds = [d for k, d in self.thresholds_per_cell.items()]
        hypamps = [d for k, d in self.hypamps_per_cell.items()]
        hyp_th['all'] = OrderedDict()
        hyp_th['all']['threshold'] = [
            round(
                numpy.mean(thresholds), 4), round(
                numpy.std(thresholds), 4)]
        hyp_th['all']['hypamp'] = [
            round(
                numpy.mean(hypamps), 4), round(
                numpy.std(hypamps), 4)]

        json.dump(
            hyp_th,
            open(
                self.maindirname +
                "hypamp_threshold.json",
                'w'),
            indent=4,
            cls=tools.NumpyEncoder)

    def create_feature_config(self, directory, dataset, version=None):
        """Save the efeatures and protocols for each protocol/target combo
        in json file"""
        logger.info(" Saving config files to %s", directory)

        if version == 'legacy':

            indent = 8
            stim = OrderedDict()
            feat = OrderedDict()

            for i_exp, expname in enumerate(self.experiments):
                if expname in dataset:
                    location = dataset[expname]['location']

                    for fi, feature in enumerate(self.features[expname]):
                        for it, target in enumerate(self.options["target"]):

                            if str(target) in dataset[expname][
                                    'mean_features'][feature]:

                                t = str(target)
                                stimname = expname + '_' + t

                                m = round(
                                    dataset[expname]['mean_features']
                                    [feature][str(target)],
                                    4)
                                s = round(
                                    dataset[expname]['std_features']
                                    [feature][str(target)],
                                    4)
                                n = int(dataset[expname]['n']
                                        [feature][str(target)])

                                if "zero_std" in self.options and \
                                        self.options["zero_std"]:
                                    rules = [~numpy.isnan(m)]
                                else:
                                    rules = [
                                        ~numpy.isnan(m), (s > 0.0) or
                                        (m == 0.0)]

                                if all(rules):
                                    if s == 0.0:  # prevent divison by 0
                                        s = 1e-3

                                    if stimname not in stim:
                                        stim[stimname] = OrderedDict()

                                    if stimname not in feat:
                                        feat[stimname] = OrderedDict()

                                    if location not in feat[stimname]:
                                        feat[stimname][location] = \
                                            OrderedDict()

                                    feat[stimname][location][feature] = [m, s]

                                    a = round(
                                        dataset[expname]['mean_amp']
                                        [str(target)],
                                        6)
                                    h = round(
                                        dataset[expname]['mean_hypamp']
                                        [str(target)],
                                        6)
                                    ton = dataset[expname]['mean_ton']
                                    toff = dataset[expname]['mean_toff']
                                    tend = dataset[expname]['mean_tend']

                                    if 'stimuli' not in stim[stimname]:

                                        totduration = round(tend)
                                        delay = round(
                                            self.options["delay"] + ton)
                                        duration = round(toff - ton)

                                        stim[stimname]['stimuli'] = [
                                            OrderedDict([
                                                ("delay", delay),
                                                ("amp", a),
                                                ("duration", duration),
                                                ("totduration", totduration),
                                            ]),
                                            OrderedDict([
                                                ("delay", 0.0),
                                                ("amp", h),
                                                ("duration", totduration),
                                                ("totduration", totduration),
                                            ]),
                                        ]

            stim = OrderedDict([(self.mainname, stim)])
            feat = OrderedDict([(self.mainname, feat)])

        else:

            indent = 6
            stim = OrderedDict()
            feat = OrderedDict()
            featraw = OrderedDict()

            boxcox = False
            if ('boxcox' in self.options) and self.options['boxcox']:
                boxcox = True

            fid = 0
            for i_exp, expname in enumerate(self.experiments):
                if expname in dataset:
                    location = dataset[expname]['location']

                    for fi, feature in enumerate(self.features[expname]):
                        for it, target in enumerate(self.options["target"]):

                            if str(target) in dataset[expname][
                                    'mean_features'][feature]:

                                t = str(target)
                                stimname = expname + '_' + t

                                m = round(
                                    dataset[expname]['mean_features']
                                    [feature][str(target)],
                                    4)
                                s = round(
                                    dataset[expname]['std_features']
                                    [feature][str(target)],
                                    4)
                                n = int(dataset[expname]['n']
                                        [feature][str(target)])

                                if self.saveraw:
                                    raw = dataset[expname]['raw'][feature][
                                        str(target)]

                                bcm = dataset[expname]['bc_mean_features'][
                                    feature][
                                    str(target)]
                                bcs = dataset[expname]['bc_std_features'][
                                    feature][
                                    str(target)]
                                bcshift = dataset[expname][
                                    'bc_shift_features'][feature][
                                    str(target)]
                                bcld = dataset[expname]['bc_ld_features'][
                                    feature][
                                    str(target)]

                                if boxcox:
                                    do_add = ~numpy.isnan(bcm)
                                else:
                                    do_add = ~numpy.isnan(m)

                                if do_add:

                                    if s == 0.0:  # prevent divison by 0
                                        s = 1e-3

                                    if bcs == 0.0:  # prevent divison by 0
                                        bcs = 1e-3

                                    if stimname not in stim:
                                        stim[stimname] = OrderedDict()

                                    if stimname not in feat:
                                        feat[stimname] = OrderedDict()
                                        featraw[stimname] = OrderedDict()

                                    if location not in feat[stimname]:
                                        feat[stimname][location] = []
                                        featraw[stimname][location] = []

                                    if boxcox and (bcshift is not False):
                                        feat[stimname][location].append(
                                            OrderedDict([
                                                ("feature", feature),
                                                ("val",
                                                 [m, s, bcm, bcs,
                                                  bcld, bcshift]),
                                                ("n", n),
                                                ("fid", fid)
                                            ]))

                                        if self.saveraw:
                                            featraw[stimname][location].append(
                                                OrderedDict([
                                                    ("feature", feature),
                                                    ("val", [m, s, bcm, bcs,
                                                             bcld, bcshift]),
                                                    ("n", n),
                                                    ("fid", fid),
                                                    ("raw", raw)
                                                ]))

                                    else:

                                        feat[stimname][location].append(
                                            OrderedDict([
                                                ("feature", feature),
                                                ("val", [m, s]),
                                                ("n", n),
                                                ("fid", fid)
                                            ]))

                                        if self.saveraw:
                                            featraw[stimname][location].append(
                                                OrderedDict([
                                                    ("feature", feature),
                                                    ("val", [m, s]),
                                                    ("n", n),
                                                    ("fid", fid),
                                                    ("raw", raw)
                                                ]))

                                    fid += 1

                                    if expname in self.options[
                                            "strict_stiminterval"].keys(
                                    ):
                                        strict_stiminterval = self.options[
                                            "strict_stiminterval"][expname]
                                    else:
                                        strict_stiminterval = self.options[
                                            "strict_stiminterval"]['base']
                                    feat[stimname][location][-1][
                                        "strict_stim"] = strict_stiminterval

                                    if self.saveraw:
                                        featraw[stimname][location][-1][
                                            "strict_stim"] = \
                                            strict_stiminterval

                                    a = round(
                                        dataset[expname]['mean_amp']
                                        [str(target)],
                                        6)
                                    h = round(
                                        dataset[expname]['mean_hypamp']
                                        [str(target)],
                                        6)
                                    threshold = round(
                                        dataset[expname]
                                        ['mean_amp_rel']
                                        [str(target)],
                                        4)
                                    ton = dataset[expname]['mean_ton']
                                    toff = dataset[expname]['mean_toff']
                                    tend = dataset[expname]['mean_tend']

                                    if 'stimuli' not in stim[stimname]:

                                        try:
                                            totduration = round(tend)
                                        except ValueError:
                                            totduration = numpy.NaN
                                        delay = round(
                                            self.options["delay"] + ton)
                                        duration = round(toff - ton)

                                        # special frequency pulse stimulus
                                        if expname == 'H40S8':
                                            n = 8
                                            duration = 2.5
                                            stim[stimname]['type'] = \
                                                'StepProtocol'
                                            stim[stimname]['stimuli'] = \
                                                OrderedDict()
                                            stim[stimname][
                                                'stimuli']['step'] = []
                                            totduration = delay + n * 25.
                                            # threshold not estimated,
                                            # used fixed values
                                            threshold = 600.

                                            for s in range(n):
                                                stim[stimname]['stimuli'][
                                                    'step'].append(
                                                    OrderedDict(
                                                        [("delay", delay + s *
                                                          25.),
                                                         ("amp", a),
                                                         ("thresh_perc",
                                                          threshold),
                                                         ("duration",
                                                          duration),
                                                         ("totduration",
                                                          totduration), ]))

                                            stim[stimname]['stimuli'][
                                                'holding'] = OrderedDict(
                                                [("delay", 0.0),
                                                 ("amp", h),
                                                 ("duration", totduration),
                                                 ("totduration",
                                                  totduration), ])
                                        else:
                                            stim[stimname]['type'] = \
                                                'StepProtocol'
                                            stim[stimname][
                                                'stimuli'] = OrderedDict([
                                                    ('step',
                                                     OrderedDict([
                                                         ("delay", delay),
                                                         ("amp", a),
                                                         ("thresh_perc",
                                                             threshold),
                                                         ("duration",
                                                             duration),
                                                         ("totduration",
                                                             totduration),
                                                     ])),
                                                    ('holding',
                                                     OrderedDict([
                                                         ("delay", 0.0),
                                                         ("amp", h),
                                                         ("duration",
                                                             totduration),
                                                         ("totduration",
                                                             totduration),
                                                     ])),
                                                ])

                    if self.is_global_features_collected:
                        # prepare feat dict for the addition of standard currents and global features
                        for current_type in self.standard_currents:
                            if current_type not in feat:
                                feat[current_type] = OrderedDict()
                            if location not in feat[current_type]:
                                feat[current_type][location] = []
                        if 'global' not in feat:
                            feat['global'] = OrderedDict()
                        if location not in feat['global']:
                            feat['global'][location] = []

                        # append standard currents and the corresponding features to the feat dict
                        for current_type in self.standard_currents:
                            # first add the mean and std of the currents themselves
                            # Use the baseline_corrected current values (expect for standard neg curr)
                            if self.correct_standard_currents_with_baseline_current:
                                if current_type != 'standard_negative_current':
                                    mean_current = dataset[expname]['mean_{}'.format(current_type + '_baseline_corrected')]
                                    std_current = dataset[expname]['std_{}'.format(current_type + '_baseline_corrected')]
                                    n_current = dataset[expname]['n_{}'.format(current_type + '_baseline_corrected')]
                                    if isinstance(mean_current, float) and isinstance(std_current, float):
                                        baseline_corrected_current_val = [round(mean_current, 4), round(std_current, 4)]
                                        #feat[current_type][location].append({"current_val_baseline_corrected": baseline_corrected_current_val, "n": n_current})
                                        #feat['global'][location].append(
                                        #    {"feature": current_type + '_baseline_corrected', "val": baseline_corrected_current_val, "n": n_current})
                                        feat[current_type][location].append({"current_val": baseline_corrected_current_val, "n": n_current})
                                        feat['global'][location].append(
                                            {"feature": current_type, "val": baseline_corrected_current_val, "n": n_current})
                                else:
                                    mean_current = dataset[expname]['mean_{}'.format(current_type)]
                                    std_current = dataset[expname]['std_{}'.format(current_type)]
                                    n_current = dataset[expname]['n_{}'.format(current_type)]
                                    if isinstance(mean_current, float) and isinstance(std_current, float):
                                        current_val = [round(mean_current, 4), round(std_current, 4)]
                                        feat[current_type][location].append(
                                            {"current_val": current_val, "n": n_current})
                                        feat['global'][location].append(
                                            {"feature": current_type, "val": current_val, "n": n_current})
                            # OR Use the NOT baseline_corrected current values (DEFAULT setting)
                            else:
                                mean_current = dataset[expname]['mean_{}'.format(current_type)]
                                std_current = dataset[expname]['std_{}'.format(current_type)]
                                n_current = dataset[expname]['n_{}'.format(current_type)]
                                if isinstance(mean_current, float) and isinstance(std_current, float):
                                    current_val = [round(mean_current, 4), round(std_current, 4)]
                                    feat[current_type][location].append({"current_val": current_val, "n": n_current})
                                    feat['global'][location].append(
                                        {"feature": current_type, "val": current_val, "n": n_current})

                            # then add the mean and std of the features belonging to said currents
                            mean_current_feat = dataset[expname]['mean_{}_features'.format(current_type)]
                            std_current_feat = dataset[expname]['std_{}_features'.format(current_type)]
                            n_current_feat = dataset[expname]['n_{}_features'.format(current_type)]
                            for feature in mean_current_feat:
                                if n_current_feat[feature]:
                                    feat_val = [round(mean_current_feat[feature], 4),
                                                round(std_current_feat[feature], 4)]
                                    feat_formatted = {"feature": feature, "val": feat_val, "n": n_current_feat[feature]}
                                    feat[current_type][location].append(feat_formatted)

                        # append global features to the feat dict
                        for global_feature in self.global_features:
                            mean_global_feature = dataset[expname]['mean_{}'.format(global_feature)]
                            std_global_feature = dataset[expname]['std_{}'.format(global_feature)]
                            n_global_feature = dataset[expname]['n_{}'.format(global_feature)]
                            if isinstance(mean_global_feature, float) and isinstance(std_global_feature, float):
                                feature_val = [round(mean_global_feature, 4), round(std_global_feature, 4)]
                                feat['global'][location].append(
                                    {"feature": global_feature, "val": feature_val, "n": n_global_feature})

        s = json.dumps(stim, indent=2, cls=tools.NumpyEncoder)
        s = tools.collapse_json(s, indent=indent)
        with open(directory + "protocols.json", "w") as f:
            f.write(s)

        s = json.dumps(feat, indent=2, cls=tools.NumpyEncoder)
        s = tools.collapse_json(s, indent=indent)
        with open(directory + "features.json", "w") as f:
            f.write(s)

        if self.saveraw:
            s = json.dumps(featraw, indent=2, cls=tools.NumpyEncoder)
            s = tools.collapse_json(s, indent=indent)
            with gzip.open(directory + "features_sources.json.gz", "wb") as f:
                f.write(s.encode('utf-8'))

    def create_metadataset(self):
        """
        Fill a dictionary with metadata for every file to be processed
        If no metadata file is present, default values are inserted
        """

        logger.info("Filling metadataset")
        path = self.path

        self.metadataset = OrderedDict()

        for i_cell, cellname in enumerate(self.cells):

            self.metadataset[cellname] = OrderedDict()
            self.metadataset[cellname]['path'] = path

            metadataset_cell_exp = OrderedDict()
            self.metadataset[cellname]['experiments'] = metadataset_cell_exp

            for i_exp, expname in enumerate(self.cells[
                    cellname]['experiments']):

                files = self.cells[cellname]['experiments'][expname]['files']

                if len(files) > 0:
                    logger.debug(" Adding experiment %s to metadata", expname)

                    metadataset_cell_exp[expname] = OrderedDict()
                    if self.format == "igor":
                        for dict_igor in files:
                            cellname = dict_igor["ordinal"]
                            foldpath = os.path.dirname(dict_igor["v_file"])
                            fullpath = os.path.join(
                                foldpath, cellname + '_' + 'metadata.json')
                            print(fullpath)
                            metadataset_cell_exp[expname][cellname] = \
                                common.manageMetadata.get_metadata(
                                fullpath)
                    else:
                        for idx_file, filename in enumerate(files):
                            fullpath = os.path.join(
                                self.path, cellname, filename + '_' +
                                'metadata.json')
                            metadataset_cell_exp[expname][filename] = \
                                common.manageMetadata.get_metadata(
                                fullpath)
        return True


