# Path: cameras/filters.py
from scipy import signal
import numpy as np
import numpy.typing as npt

class Filters:
    #TODO: add buffer
    def __init__(self):
        pass

    def butterLowPass2D(x : npt.NDArray[np.float64], cutoff : float, fs : float, order=5 : int):
        """
        Inputs:
            u: 2-d numpy array containing the input signal to be filtered
            cutoff: number between 0 and 1
            fs: sampling frequency
            order: integer
        Outputs:
            numpy array - 2-d numpy array containing the filtered signal
        """
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
        y = signal.filtfilt(b, a, x, axis=0) # lfilt is slow   FIXME: why am i overwriting y?
        y = signal.filtfilt(b, a, y, axis=1)
        return y

    def causalLowPass(x : npt.NDArray[np.float64], alpha : float):
        """
        Inputs:
            u: 1-d numpy array containing the input signal to be filtered
            alpha: number between 0 and 1
        Outputs:
            numpy array - 1-d numpy array containing the filtered signal
        """
        y = signal.lfilter([1 - alpha], [1, -alpha], x)
        return y

    def causalLowPass2D(x : npt.NDArrray[np.float64], cutoff : float, fs : float, order=5 : int):
        """
        Inputs:
            u: 2-d numpy array containing the input signal to be filtered
            cutoff: number between 0 and 1
            fs: sampling frequency
            order: integer
        Outputs:
            numpy array - 2-d numpy array containing the filtered signal
        """
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
        y = signal.lfilter(b, a, x, axis=0) # lfilt is slow
        y = signal.lfilter(b, a, y, axis=1)
        return y


    def nonCausalLowPass(x : npt.NDArray[np.float64], alpha : float):
        """
        Inputs:
            u: 1-d numpy array containing the input signal to be filtered
            alpha: number between 0 and 1
        Outputs:
            numpy array - 1-d numpy array containing the filtered signal
        """
        y = signal.filtfilt([1 - alpha], [1, -alpha], x)
        return y
        

    def make_square(frame : npt.NDArray[np.float64]):
        #  make the frame square by cropping the longer side
        h, w = frame.shape[:2]
        if h > w:
            return frame[(h-w)//2:(h+w)//2, :]
        else:
            return frame[:, (w-h)//2:(w+h)//2]
        

