from deprecated import deprecated
from pathlib import Path
from datetime import datetime

from matplotlib import gridspec, pyplot as plt
import librosa
import numpy as np
from numpy import ndarray as array
from scipy.signal import argrelextrema, find_peaks_cwt, find_peaks
import soundfile as sf
from IPython.display import Audio

from core.model.song import Song
from core.logger import Logger, LOG_CAT


class Common():

    @staticmethod
    def computeAttribs(song: Song, stem: str) -> dict:
        """
        WRITE

        Args:
            song (soundlight.model.song.Song): Song data
            stem (str): Steam name to process

        Returns:
            dict: _description_
        """
        attribs = {}

        # > TinyTag metadata
        attribs['track_length'] = song.metadata['tinytag']['duration']
        attribs['sr'] = song.metadata['tinytag']['samplerate'] if song.metadata['tinytag']['samplerate'] else None
        attribs['bpm'] = song.metadata['tinytag']['bpm'][0] if song.metadata['tinytag']['bpm'][0] else song.metadata['aio']['bpm']

        # > AIO metadata
        attribs['downbeats'] = song.metadata['aio']['downbeats']
        attribs['phrases'] = song.metadata['aio']['segments']
        attribs['stem_path'] = song.metadata['aio']['demucs'][stem]

        # Calculate samples per beat as time signature 4/4
        attribs['beat_sample_length'] = (
            (attribs['sr'] * 60) / int(attribs['bpm'])) * 4

        return attribs

    @staticmethod
    def load(attribs: dict) -> tuple[array, int]:
        """
        WRITE

        Args:
            attribs (dict): _description_

        Returns:
            array: _description_
            int: _description_
        """
        # Load stem
        y, sr = librosa.load(
            attribs['stem_path'], sr=attribs['sr'])

        return y, sr

    @staticmethod
    def getRMS(data: array, rmsParams: dict | None = None) -> array:
        """
        WRITE

        Args:
            data (array): _description_
            rmsParams (dict): 'frame_length' and 'hop_length' required, else runs with 2048 and 512.

        Returns:
            array: _description_
        """
        if rmsParams:
            return librosa.feature.rms(y=data, frame_length=rmsParams['frame_length'], hop_length=rmsParams['hop_length'])[0]
        else:
            return librosa.feature.rms(y=data)[0]

    @staticmethod
    def scale(data: array, scale: tuple[int, int] = (0, 1)) -> array:
        min = scale[0]
        max = scale[1]
        data_min = np.min(data)
        data_max = np.max(data)

        return ((data - data_min) / (data_max - data_min)) * (max - min) + min

    @staticmethod
    def timestampToIndexOf(data: array, timestamps: array, data_duration: float) -> array:
        """Converts a list of timestamps into a list of indexes of `data`. Takes each timestamp from `timestamps` and converts it into the corresponding index of data, such that it aligns.

        WRITE
        Args:
            data (array): _description_
            timestamps (array): _description_
            data_duration (float): _description_

        Returns:
            array: _description_
        """
        ret = []

        for ts in timestamps:
            # FIXME: What if ts is greater than data_duration?
            ts_percentage = ts / data_duration
            ret.append(int(ts_percentage * len(data)))

        return np.asarray(ret)

    @staticmethod
    def getPeakIndexes(data: array, peakArgs: dict | None = None, peakFunction: str = 'argrelextrema') -> tuple[array, array]:
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
    def filterWith(data: array, data_i: array, filter: callable) -> array:
        ret = []

        for i in data_i:
            if filter(data, i):
                ret.append(i)

        return np.asarray(ret)

    @staticmethod
    def filterThresholds(data: array, filter: dict, maxima_i: array | None = None, minima_i: array | None = None) -> tuple[array, array] | array | None:

        # TODO: Refactor to receive only one array and to use a comparator

        # Filter for high and low threshold
        if maxima_i is not None:
            maxima_i = [i for i in maxima_i if data[i] >= filter['high']]
            # maxima_i = np.where(data[maxima_i] >= thresholds['high'])
        if minima_i is not None:
            minima_i = [i for i in minima_i if data[i] <= filter['low']]
            # minima_i = np.where(data[minima_i] <= thresholds['low'])

        # print(f'Lengths after: {len(maxima_i)}, {len(minima_i)}')
        if maxima_i is not None and minima_i is not None:
            return maxima_i, minima_i
        elif maxima_i is not None:
            return maxima_i
        elif minima_i is not None:
            return minima_i
        else:
            return None

    @staticmethod
    def _localCompare(i: int, y: array, maxima_i: array, minima_i: array, distance: float) -> bool:
        lmax: float = y[maxima_i[i]]

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
    def split(audio: np.ndarray, start_indexes: list[int]) -> tuple[list[array], list[array]]:
        """Splits the audio into sections, according to the start indexes for the sections, and returns a list of arrays, with each array corresponding to a section.

        Args:
            data (np.ndarray): The audio data time series
            start_indexes (list[int]): Indexes where the section starts

        Returns:
            list[array], list[array]: list of np.ndarrays. Each array in the list contains one section. The first list contains the values, the second contains the indexes relative to the original data
        """

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

        return ret, ret_i

    @staticmethod
    def display(data: array, peaks_i: array | None = None, valleys_i: array | None = None, thresholds: dict | list | None = None, section_i: dict | None = None, figsize: tuple[int, int] = (36, 3), save: bool = False, reg_line: np.poly1d | bool | None = None):
        """_summary_

        Args:
            data (array): _description_
            maxima_indexes (array): _description_
            minima_indexes (array | None, optional): _description_. Defaults to None.
            thresholds (dict | None, optional): _description_. Defaults to None.
            section_dict (dict | None, optional): _description_. Defaults to None.
            figsize (tuple(int, int), optional): Dimensions of the figure.
        """

        Logger.log(LOG_CAT.INFO, f'Visualizing data...')
        plt.figure(figsize=figsize)

        # Plot data
        plt.plot(data, color='black', linewidth=1)
        plt.xlim(0, len(data))
        if np.max(data) != 1.0 or np.min(data) != 0:
            Logger.log(
                LOG_CAT.WARN, f'Data does not appear to be normalized. Plot can be innacurate.')
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
                Logger.log(LOG_CAT.INFO, 'Plotting section thresholds...')

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
        if save:
            Logger.log(LOG_CAT.INFO, 'Saving to file...')
            plt.savefig(
                f'/home/alvaro/Escritorio/SoundLight/SoundLight/output/bass_{datetime.now()}.pdf')

        Logger.log(LOG_CAT.SUCCESS, f'Finished visualizing.')

    @staticmethod
    def sonify(data: array, sr: int, peaks: array | None = None,  save: bool = False) -> Audio:
        if peaks is None:
            return Audio(data=data, rate=sr)
        else:

            newdata: array = np.copy(data)
            beep_duration = 0.2  # 200ms
            # Convert duration to samples
            beep_samples = int(beep_duration * sr)
            beep_sound = librosa.tone(
                1000, sr=sr, duration=beep_duration) * 0.25

            for peak_i in peaks:
                end_i = min(peak_i + beep_samples, len(newdata))
                # Add beep to the original signal
                newdata[peak_i:end_i] += beep_sound[: end_i - peak_i]

            if save:
                sf.write(
                    r"/home/alvaro/Escritorio/SoundLight/SoundLight/output/bass.wav", newdata, sr)

            return Audio(data=newdata, rate=sr)
