from typing import List
from deprecated import deprecated
from pathlib import Path
from datetime import datetime
from collections.abc import Callable

from matplotlib import gridspec, pyplot as plt
import librosa
import numpy as np
from numpy import ndarray as array
from scipy.signal import argrelextrema, find_peaks_cwt, find_peaks
import soundfile as sf
from IPython.display import Audio

from ...conf import Conf
from ...model.song import Song
from ...logger import Logger, LOG_CAT


class Common():
    """Contains useful functions for audio analysis. Mainly used in BassAnalysis.
    This class should either be refactored in the future, to make it more reusable; or removed and its code distributed among the classes that use it, if it is too specific.
    """

    @staticmethod
    def compute_attribs(song: Song, stem: str) -> dict:
        """
        Computes the required attributes for the song, given the stem under analysis.

        Args:
            song (soundlight.model.song.Song): Song data
            stem (str): Steam name to process

        Returns:
            dict: _description_
        """
        attribs: dict = {}

        # > TinyTag metadata
        attribs['track_length'] = song['metadata']['tinytag']['duration']
        attribs['sr'] = song['metadata']['tinytag']['samplerate'] if song['metadata']['tinytag']['samplerate'] else None
        if 'bpm' in song['metadata']['tinytag'] and song['metadata']['tinytag']['bpm'][0]:
            attribs['bpm'] = song['metadata']['tinytag']['bpm'][0]
        else:
            attribs['bpm'] = song['metadata']['aio']['bpm']

        # attribs['bpm'] = song['metadata']['tinytag']['bpm'][0] if song['metadata']['tinytag']['bpm'] else song['metadata']['aio']['bpm']

        # > AIO metadata
        attribs['downbeats'] = song['metadata']['aio']['downbeats']
        attribs['phrases'] = song['metadata']['aio']['segments']
        attribs['stem_path'] = song['metadata']['aio']['demucs'][stem]

        # Calculate samples per beat as time signature 4/4
        attribs['beat_sample_length'] = (
            (attribs['sr'] * 60) / int(attribs['bpm'])) * 4  # type: ignore

        return attribs

    @staticmethod
    def load(attribs: dict) -> tuple[array, int]:
        """Loads a song from its path.

        Args:
            attribs (dict): Must contain a key 'stem_path' with the path to the song.

        Returns:
            array: Song data
            int: Sample rate
        """
        # Load stem
        y, sr = librosa.load(
            attribs['stem_path'], sr=attribs['sr'])

        return y, int(sr)

    @staticmethod
    def get_rms(data: array, rmsParams: dict | None = None) -> array:
        """Calculates the RMS profile for the data.

        Args:
            data (array): Data for which to calculate RMS.
            rmsParams (dict): 'frame_length' and 'hop_length' required, else runs with 2048 and 512.

        Returns:
            array: RMS data. The number of samples is always smaller than the original.
        """
        if rmsParams:
            return librosa.feature.rms(y=data, frame_length=rmsParams['frame_length'], hop_length=rmsParams['hop_length'])[0]
        else:
            return librosa.feature.rms(y=data)[0]

    @staticmethod
    def scale(data: array, scale: tuple[int, int] = (0, 1)) -> array:
        """Linearly scales the given data between the specified minimum and maximum values.

        Args:
            data (array): Data to scale.
            scale (tuple[int, int], optional): Tuple containing the minimum and maximum to scale. Defaults to (0, 1).

        Returns:
            array: _description_
        """
        min = scale[0]
        max = scale[1]
        data_min = np.min(data)
        data_max = np.max(data)

        return ((data - data_min) / (data_max - data_min)) * (max - min) + min

    @staticmethod
    def timestamp_to_index_of(data: array, timestamps: array, data_duration: float) -> array:
        """Converts a list of timestamps into a list of indexes of `data`. Takes each timestamp from `timestamps` and converts it into the corresponding index of data, such that it aligns.
        """
        ret = []

        for ts in timestamps:
            # FIXME: What if ts is greater than data_duration?
            ts_percentage = ts / data_duration
            ret.append(int(ts_percentage * len(data)))

        return np.asarray(ret)

    @staticmethod
    def get_peak_indexes(data: array, peakArgs: dict | None = None, peakFunction: str = 'argrelextrema') -> tuple[array, array]:
        """Obtains the indexes of peaks, based on the thresholds and the peak function chosen.

        Args:
            y (array): _description_
            peakArgs (dict): _description_

        Returns:
            tuple(array, array): ``maxima_i`` and ``minima_i``
        """

        # We find the peaks
        match peakFunction:
            case 'argrelextrema':
                peaks_i: array = argrelextrema(data, np.greater)[0]
                valleys_i: array = argrelextrema(data, np.less)[0]
            case 'cwt':
                raise NotImplementedError(
                    'core.analysis.stems.common.Common.getPeaks')
                peaks_i: array = find_peaks_cwt(data, widths=100)
            case 'peaks':
                raise NotImplementedError(
                    'core.analysis.stems.common.Common.getPeaks')
                peaks_i: array = find_peaks(data)
            case _:
                peaks_i: array = argrelextrema(data, np.greater)[0]
                valleys_i: array = argrelextrema(data, np.less)[0]

        return peaks_i, valleys_i

    @staticmethod
    def filter_with(data: array, filter: Callable, data_i: array | None = None) -> array:
        """Filters an array of data given the filtering function provided.

        Args:
            data (array): Data to filter.
            filter (Callable): Filter function, that takes as parameter a single element of ``data``
            data_i (array | None, optional): Array of specific indexes to filter. Defaults to None (filter all elements).

        Returns:
            array: Array with only the elements for which ``filter`` returns True.
        """
        ret = []
        if data_i:
            for i in data_i:
                if filter(data, i):
                    ret.append(i)
        else:
            for i in range(len(data)):
                if filter(data, i):
                    ret.append(i)

        return np.asarray(ret)

    @staticmethod
    @deprecated
    def filter_thresholds(data: array, filter: dict, maxima_i: array | None = None, minima_i: array | None = None) -> tuple[array, array] | array | None:
        """DEPRECATED: Use filterWith()
        Filters an array of data given the 'high' and 'low' values on the filter.

        Args:
            data (array): _description_
            filter (dict): _description_
            maxima_i (array | None, optional): _description_. Defaults to None.
            minima_i (array | None, optional): _description_. Defaults to None.

        Returns:
            tuple[array, array] | array | None: _description_
        """

        # TODO: Refactor to receive only one array and to use a comparator

        # Filter for high and low threshold
        if maxima_i is not None:
            maxima_i = [i for i in maxima_i if data[i]
                        >= filter['high']]  # type: ignore
            # maxima_i = np.where(data[maxima_i] >= thresholds['high'])
        if minima_i is not None:
            minima_i = [i for i in minima_i if data[i]
                        <= filter['low']]  # type: ignore
            # minima_i = np.where(data[minima_i] <= thresholds['low'])

        if maxima_i is not None and minima_i is not None:
            return maxima_i, minima_i
        elif maxima_i is not None:
            return maxima_i
        elif minima_i is not None:
            return minima_i
        else:
            return None

    @staticmethod
    @deprecated
    def _local_compare(i: int, y: array, maxima_i: array, minima_i: array, distance: float) -> bool:
        """DEPRECATED

        Args:
            i (int): _description_
            y (array): _description_
            maxima_i (array): _description_
            minima_i (array): _description_
            distance (float): _description_

        Returns:
            bool: _description_
        """
        lmax: float = y[maxima_i[i]]  # type: ignore

        # Checking out of bounds:
        if i < 1 or i > (len(minima_i)-1):
            return False

        # Comparison
        if abs(lmax - y[minima_i[i-1]]) < distance:
            return False
        elif abs(lmax - y[minima_i[i]]) < distance:
            return False
        elif abs(lmax - y[minima_i[i+1]]) < distance:
            return False
        elif lmax < distance:
            return False
        else:
            return True

    @staticmethod
    def split(audio: np.ndarray, start_indexes: List[int]) -> tuple[List[array], List[array]]:
        """Splits the audio into sections, according to the start indexes for the sections, and returns a list of arrays, with each array corresponding to a section.

        Args:
            data (np.ndarray): The audio data time series
            start_indexes (List[int]): Indexes where the section starts

        Returns:
            List[array], List[array]: list of np.ndarrays. Each array in the list contains one section. The first list contains the values, the second contains the indexes relative to the original data
        """

        # TODO: This could be coded cleaner with the zip() method

        ret = []    # Samples
        ret_i = []  # Sample indexes

        prev = 0
        # For each section start:
        for i in start_indexes:
            if i == 0:
                continue    # If there is a section starting at the beginning, skip
            section = audio[prev:i]
            section_is = np.asarray([j for j in range(prev, i)])

            ret.append(section)
            ret_i.append(section_is)

            prev = i

        # Last section
        section = audio[prev:]
        section_is = np.asarray([j for j in range(prev, len(audio))])

        ret.append(section)
        ret_i.append(section_is)

        # if len(ret) == len(ret_i):
        #   return zip(ret_i, ret)
        # else:

        return ret, ret_i

    @staticmethod
    def display(data: array, peaks_i: array | None = None, valleys_i: array | None = None, thresholds: dict | list | None = None, section_i: dict | None = None, figsize: tuple[int, int] = (36, 3), save: Path | None = None, reg_line: np.poly1d | bool | None = None):
        """_summary_

        ADisplays the results.

        Args:
            data (array): Data to display.
            maxima_indexes (array): Indexes of the peaks.
            minima_indexes (array | None, optional): Indexes of the valleys.
            thresholds (dict | None, optional): Thresholds used.
            section_dict (dict | None, optional): Contains the song sections.
            figsize (tuple(int, int), optional): Dimensions of the figure.
            save (Path | None, optional): If present, path in which to save the rendered image.
            reg_line (np.poly1d | bool | None, optional): Regression line.
        """

        Logger.log(LOG_CAT.INFO, f'Visualizing data...')
        plt.figure(figsize=figsize)

        # Plot data
        plt.plot(data, color='black', linewidth=1)
        plt.xlim(0, len(data))
        if np.max(data) != 1.0 or np.min(data) != 0:
            Logger.log(
                LOG_CAT.WARN, f'Data does not appear to be normalized. Plot can be innacurate.')
            pass
        plt.ylim(0, 1.1)
        plt.ylabel('Data')

        # Plot peaks
        if peaks_i is not None:
            Logger.log(LOG_CAT.INFO, 'Plotting peaks...')
            peak_values = []
            for i in peaks_i:
                peak_values.append(data[int(i)])
            plt.scatter(
                peaks_i, peak_values, color='red', label='Peaks', zorder=3)

        # Plot valleys
        if valleys_i is not None:
            Logger.log(LOG_CAT.INFO, 'Plotting valleys...')
            valley_values = []
            for i in valleys_i:
                valley_values.append(data[i])
            plt.scatter(
                valleys_i, valley_values, color='green', label='Minima', zorder=3)

        # Print thresholds
        if thresholds is not None:
            if type(thresholds) is list:
                Logger.log(
                    LOG_CAT.INFO, 'Plotti_summary_ng section thresholds...')

                for section in thresholds:
                    if 'low' in section:
                        plt.axhline(y=section['low'], xmin=section['xmin'] / len(
                            data), xmax=section['xmax'] / len(data), color='green', linestyle='dotted')
                    if 'high' in section:
                        plt.axhline(y=section['high'], xmin=section['xmin'] / len(
                            data), xmax=section['xmax'] / len(data), color='red', linestyle='dotted')

            elif type(thresholds) is dict:
                Logger.log(LOG_CAT.INFO, 'Plotting general threshold...')
                if 'low' in thresholds:
                    plt.axhline(y=thresholds['low'],
                                color='green', linestyle='dotted')
                if 'high' in thresholds:
                    plt.axhline(y=thresholds['high'],
                                color='red', linestyle='dotted')

            else:
                Logger.log(
                    LOG_CAT.WARN, f'Unexpected object for `thresholds`: {type(thresholds)}')
                pass

        # Print section
        if section_i is not None:
            Logger.log(LOG_CAT.INFO, 'Plotting sections...')
            # Section lines
            for i in section_i:
                plt.axvline(x=i, color='black', linestyle='-')

        # Print regression line
        if reg_line is not None:
            # Sectioned regression lines
            if reg_line is True:
                Logger.log(
                    LOG_CAT.INFO, f'Plotting sectioned regression lines...')
                if thresholds is not None and type(thresholds) is list:
                    for th in thresholds:
                        if 'reg_line' in th:
                            d = np.asarray(
                                [i for i in range(th['xmin'], th['xmax'])])
                            plt.plot(d, th['reg_line'](d), color='b')
            # Single regression line
            elif type(reg_line) is np.poly1d:
                Logger.log(LOG_CAT.INFO, f'Plotting single regression line...')
                d = [i for i in range(len(data))]
                plt.plot(d, reg_line(d), color='b')

        # Save figure:
        if save is not None:
            Logger.log(LOG_CAT.INFO, 'Saving to file...')
            plt.savefig(f'{save}/{datetime.now()}.pdf')

        Logger.log(LOG_CAT.SUCCESS, f'Finished visualizing.')

    @staticmethod
    def sonify(data: array, sr: int, peaks: array | None = None,  save: Path | None = None) -> Audio:
        """Sonifies the peaks in the audio.

        Args:
            data (array): Original audio.
            sr (int): Sample rate of the audio.
            peaks (array | None, optional): Peaks to show.
            save (Path | None, optional): If present, path in which to save the sonified audio.

        Returns:
            Audio: _description_
        """
        if peaks is None:
            return Audio(data=data, rate=sr)
        else:
            peaks = np.array([int(f) for f in peaks])
            newdata: array = np.copy(data)
            beep_duration = 0.2  # 200ms

            # Convert duration to samples
            beep_samples = int(beep_duration * sr)
            beep_sound = librosa.tone(
                1000, sr=sr, duration=beep_duration) * 0.25

            for peak_i in peaks:
                end_i = int(min(peak_i + beep_samples, len(newdata)))
                # Add beep to the original signal
                newdata[peak_i:end_i] += beep_sound[: end_i - peak_i]

            if save:
                sf.write(save, newdata, sr)

            return Audio(data=newdata, rate=sr)
