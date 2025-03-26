

import numpy as np
from numpy import ndarray as array
import librosa
from allin1.typings import Segment

from core.analysis.stems.common import Common
from core.logger import LOG_CAT, Logger
from core.model.song import Song


class BassAnalysis():

    _THRESHOLD_PERCENTAGE: float = 0.025
    _RMSPARAMS: dict[str, int] = {'frame_length': 4096, 'hop_length': 1024}
    # _RMSPARAMS: dict[str, int] = {'frame_length': 1024, 'hop_length': 1024}

    def __init__(self, song: Song) -> None:

        self._song: Song = song
        self._attribs: dict
        self._data: dict = {}

    def analyze(self, display: bool = False, sonify: bool = False) -> array:
        """Analyzes the bass stem of the song, to get peaks

        Returns:
            np.ndarray: Array with the indexes of the detected peaks
        """
        # Load song data
        self._attribs = Common.computeAttribs(self._song, 'bass')
        self._data['song_data'], _ = Common.load(
            self._attribs)  # array: Array with all samples

        # Configuring RMS params
        bass_rms_params: dict[str, int] = {
            'frame_length': 8192, 'hop_length': 2048}
        rms_data: array = Common.getRMS(
            self._data['song_data'], bass_rms_params)
        rms_data = Common.scale(rms_data)

        # Divide song in phrases
        i: Segment
        phrase_starts = [i.start for i in self._attribs['phrases']]
        phrase_indexes = Common.timestampToIndexOf(
            rms_data, phrase_starts, self._attribs['track_length'])
        phrases, phrases_i = Common.split(rms_data, phrase_indexes)

        # Analyze each phrase
        all_peaks_i = []
        all_filters = []

        filter_str: str = 'hybrid'
        for p_i in range(len(phrases)):
            self._analyzePhrase(phrases, phrases_i,
                                all_peaks_i, all_filters, filter_str, p_i)

        # Converting RMS indexes to song indexes
        peaks = np.concatenate(all_peaks_i) * \
            (len(self._data['song_data']) // len(rms_data))

        # Adjusting factor
        peaks += int(self._attribs['sr'] * 0.0)

        if sonify:
            Common.sonify(self._data['song_data'],
                          self._attribs['sr'], peaks=peaks, save=True)

        if display:
            Common.display(data=rms_data, peaks_i=np.concatenate(all_peaks_i))

        return peaks

    def _analyzePhrase(self, phrases, phrases_i, all_peaks_i, all_filters, filter_str, p_i) -> None:
        phrase = phrases[p_i]
        phrase_i = phrases_i[p_i]

        # We get the peaks from the phrase samples
        p_peak_i, _ = Common.getPeakIndexes(phrase)

        # Analyze and filter
        match filter_str:
            case 'threshold':
                # We calculate the threshold as above the mean of the samples
                th_mean = np.mean(phrase)
                filter_d = {
                    'xmin': phrase_i[0], 'xmax': phrase_i[-1], 'high': float(th_mean)}

                # We filter the peaks with this threshold
                p_peak_i = Common.filterThresholds(phrase, filter_d, p_peak_i)
            case 'reg_line':
                # We calculate the regression line for the phrase samples
                reg_line = np.poly1d(np.polyfit(
                    [i+phrase_i[0] for i in range(len(phrase))], phrase, 1))

                def filter(arr: array, i: int):
                    return arr[i] >= reg_line(i)
                    # Filter all below regression line
                p_peak_i = Common.filterWith(
                    data=phrase, data_i=p_peak_i, filter=filter)
                filter_d = {'reg_line': reg_line}
            case 'hybrid':
                # We calculate the threshold as above the mean of the samples
                th_mean = np.mean(phrase)
                filter_d = {
                    'xmin': phrase_i[0], 'xmax': phrase_i[-1], 'high': float(th_mean)}

                # We filter the peaks with this threshold
                p_peak_i = Common.filterThresholds(phrase, filter_d, p_peak_i)

                # We calculate the regression line for the phrase samples
                reg_line = np.poly1d(np.polyfit(
                    [i for i in range(len(phrase))], phrase, 1))

                def filter(arr: array, i: int):
                    return arr[i] >= reg_line(i)
                    # Filter the phrase samples with the regression line
                p_peak_i = Common.filterWith(
                    data=phrase, data_i=p_peak_i, filter=filter)

                # Adjust regression line with correct indexes
                reg_line = np.poly1d(np.polyfit(phrase_i, phrase, 1))
                filter_d['reg_line'] = reg_line
            case _:
                pass

            # Adjusting peak offset
        p_peak_i += phrase_i[0]

        # Save results
        all_peaks_i.append(p_peak_i)
        all_filters.append(filter_d.copy())

    def _analyzeBeat(self, beat: array, i_beat: array) -> array:
        """Obtains the sound peaks for this beat

        Args:
            beat (array): Beat samples
            i_beat (array): Sample indexes of the beat

        Returns:
            array: _description_
        """
        # 1. Obtain RMS of beat
        beat_rms: array = Common.getRMS(beat, self._RMSPARAMS)

        # 2. Get all peaks
        peaks_i, _ = Common.getPeakIndexes(beat_rms, None)
        peaks_i = peaks_i * int(len(beat)/len(beat_rms))   # Scaling indexes
        # Adjusting indexes
        peaks_i = peaks_i + i_beat[0]

        # 3. Trim peaks
        threshold_low = 0.25
        threshold_high = 0.75
        thresholds = {'low': threshold_low, 'high': threshold_high,
                      'compare': self._THRESHOLD_PERCENTAGE}
        self._attribs['thresholds'] = thresholds
        peaks_i = Common.filterWith(beat, peaks_i, None, thresholds)

        return peaks_i
