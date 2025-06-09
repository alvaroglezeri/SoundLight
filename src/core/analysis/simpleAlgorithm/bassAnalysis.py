from pathlib import Path
from typing import List
from deprecated import deprecated
import numpy as np
from numpy import ndarray as array


from ...analysis.simpleAlgorithm.common import Common
from ...conf import Conf
from ...model.song import Song


class BassAnalysis():
    """Detects the peaks in the bass stem of a song.
    """

    def __init__(self, song: Song) -> None:
        """Creates the BassAnalysis object

        Args:
            song (Song): Song object, with the bass stem analyzed
        """

        self._song: Song = song
        self._attribs: dict
        self._data: dict = {}

        # Loading configuration parameters
        self._THRESHOLD_PERCENTAGE = Conf(
        )['analysis']['simpleAlgorithm']['bass']['threshold_percentage']
        self._RMSPARAMS = Conf()[
            'analysis']['simpleAlgorithm']['bass']['rms_params']
        self._SONIFY = Conf()[
            'analysis']['simpleAlgorithm']['bass']['sonify']
        self._DISPLAY = Conf()[
            'analysis']['simpleAlgorithm']['bass']['display']
        self._SAVE_DIR = Conf()[
            'analysis']['simpleAlgorithm']['bass']['save_dir']

    # ----------------------------------------------------------------------------------

    def analyze(self) -> array:
        """Analyzes the bass stem of the song, to get its volume peaks.

        Returns:
            np.ndarray: Array with the indexes of the detected peaks.
        """
        self._load_song_data()
        rms_data = self._get_rms()
        phrases, phrases_i = self._get_phrases(rms_data)

        # TODO: Cleanup and divide this code into smaller functions

        # Analyze each phrase
        all_peaks_i = []
        all_filters = []

        filter_mode: str = 'hybrid'
        for p_i in range(len(phrases)):
            self._analyze_phrase(phrases, phrases_i,
                                 all_peaks_i, all_filters, filter_mode, p_i)

        # Converting RMS indexes to song indexes
        peaks = np.concatenate(all_peaks_i) * \
            (len(self._data['song_data']) // len(rms_data))

        # Adjusting factor
        peaks += int(self._attribs['sr'] * 0.0)

        if self._SONIFY:
            Common.sonify(self._data['song_data'],
                          self._attribs['sr'], peaks=peaks, save=Path(f'{self._SAVE_DIR}/bass.wav'))

        if self._DISPLAY:
            Common.display(data=rms_data, peaks_i=np.concatenate(
                all_peaks_i), save=Path(self._SAVE_DIR))

        return peaks

    # ----------------------------------------------------------------------------------

    def _load_song_data(self) -> None:
        """Translates the song data into a custom data structure, to simplify processing.
        """
        # Load song data
        self._attribs = Common.compute_attribs(self._song, 'bass')
        self._data['song_data'], _ = Common.load(
            self._attribs)  # array: Array with all samples

    def _get_rms(self) -> array:
        """Computes the RMS profile for the song, which better outlines the volume of each section.

        Returns:
            array: RMS data for the song, scaled between 0 and 1. The number of samples of the RMS data is lower than the original number of samples.
        """
        # Configuring RMS params
        rms_data: array = Common.get_rms(
            self._data['song_data'], self._RMSPARAMS)
        return Common.scale(rms_data)

    def _get_phrases(self, rms_data) -> tuple[List[array], List[array]]:
        """Splits the RMS data by section phrases.

        Args:
            rms_data (_type_): Data to split.

        Returns:
            tuple[List[array], List[array]]: List of section data and list of section indexes.
        """
        # Divide song in phrases
        phrase_starts = [i.start for i in self._attribs['phrases']]
        phrase_indexes = Common.timestamp_to_index_of(
            rms_data, phrase_starts, self._attribs['track_length'])  # type: ignore
        # TODO: This could be coded cleaner with the zip() method
        return Common.split(rms_data, phrase_indexes)  # type: ignore

    # ----------------------------------------------------------------------------------

    def _analyze_phrase(self, phrases, phrases_i, all_peaks_i, all_filters, filter_mode, p_i) -> None:
        """Analyzes each phrase, to give context to the analysis and allow finer threshold adjustments.
        """
        phrase = phrases[p_i]
        phrase_i = phrases_i[p_i]

        # We get the peaks from the phrase samples
        p_peak_i, _ = Common.get_peak_indexes(phrase)

        # Analyze and filter
        # TODO: Cleanup this code, extract to individual methods.
        match filter_mode:
            case 'threshold':
                # We calculate the threshold as above the mean of the samples
                th_mean = np.mean(phrase)
                filter_d = {
                    'xmin': phrase_i[0], 'xmax': phrase_i[-1], 'high': float(th_mean)}

                # We filter the peaks with this threshold
                p_peak_i = Common.filter_thresholds(phrase, filter_d, p_peak_i)
            case 'reg_line':
                # We calculate the regression line for the phrase samples
                reg_line = np.poly1d(np.polyfit(
                    [i+phrase_i[0] for i in range(len(phrase))], phrase, 1))

                def filter(arr: array, i: int):
                    return arr[i] >= reg_line(i)
                    # Filter all below regression line
                p_peak_i = Common.filter_with(
                    data=phrase, data_i=p_peak_i, filter=filter)
                filter_d = {'reg_line': reg_line}
            case 'hybrid':
                # We calculate the threshold as above the mean of the samples
                th_mean = np.mean(phrase)
                filter_d = {
                    'xmin': phrase_i[0], 'xmax': phrase_i[-1], 'high': float(th_mean)}

                # We filter the peaks with this threshold
                p_peak_i = Common.filter_thresholds(phrase, filter_d, p_peak_i)

                # We calculate the regression line for the phrase samples
                reg_line = np.poly1d(np.polyfit(
                    [i for i in range(len(phrase))], phrase, 1))

                def filter(arr: array, i: int):
                    return arr[i] >= reg_line(i)
                    # Filter the phrase samples with the regression line
                p_peak_i = Common.filter_with(
                    data=phrase, data_i=p_peak_i, filter=filter)  # type: ignore

                # Adjust regression line with correct indexes
                reg_line = np.poly1d(np.polyfit(phrase_i, phrase, 1))
                filter_d['reg_line'] = reg_line
            case _:
                filter_d = {}
                pass

            # Adjusting peak offset
        p_peak_i += phrase_i[0]

        # Save results
        all_peaks_i.append(p_peak_i)
        all_filters.append(filter_d.copy())

    # ----------------------------------------------------------------------------------

    @deprecated
    def _analyze_beat(self, beat: array, i_beat: array) -> array:
        """Obtains the sound peaks for this beat

        Args:
            beat (array): Beat samples
            i_beat (array): Sample indexes of the beat

        Returns:
            array: _description_
        """
        # 1. Obtain RMS of beat
        beat_rms: array = Common.get_rms(beat, self._RMSPARAMS)

        # 2. Get all peaks
        peaks_i, _ = Common.get_peak_indexes(beat_rms, None)
        peaks_i = peaks_i * int(len(beat)/len(beat_rms))   # Scaling indexes
        # Adjusting indexes
        peaks_i = peaks_i + i_beat[0]

        # 3. Trim peaks
        threshold_low = 0.25
        threshold_high = 0.75
        thresholds = {'low': threshold_low, 'high': threshold_high,
                      'compare': self._THRESHOLD_PERCENTAGE}
        self._attribs['thresholds'] = thresholds
        # peaks_i = Common.filterWith(beat, peaks_i, None, thresholds)
        peaks_i = Common.filter_thresholds(beat, thresholds, peaks_i, None)

        return peaks_i  # type: ignore
