from scipy.io import wavfile
import numpy as np
import wave


class PreProcessing:
    def npToList(self, signal):
        try:
            signal = signal[:, 0]
        except IndexError as err:
            pass
        new_signal = []
        for s in signal:
            new_signal.append(s)
        return new_signal

    def find_mean(self, sig):
        signal = list(sig)
        total = 0
        for i in range(len(signal)):
            total += signal[i]
        return total / len(signal)

    def zero_mean(self, sig):
        signal = list(sig)
        mean = self.find_mean(signal)
        # Assign new value
        for i in range(len(signal)):
            signal[i] -= mean
        return signal

    def normalization(self, sig):
        signal = list(sig)
        new_signal = []
        signal_max = signal[0]
        for i in range(len(signal)):
            if signal[i] > signal_max:
                signal_max = signal[i]
        for i in range(len(signal)):
            signal[i] /= signal_max
        return signal

    def autoFixedLength(self, sig):
        signal = list(sig)
        length = (len(signal) // 256 + 1) * 256
        return self.fixedLength(signal, length)

    def fixedLength(self, sig, length):
        signal = list(sig)
        if len(signal) > length:
            return signal[:length]
        elif len(signal) < length:
            for _ in range(length - len(signal)):
                signal.append(0)
        return signal

    def power(self, sig):
        signal = list(sig)
        new_signal = []
        for i in range(len(signal)):
            new_signal.append(signal[i] ** 2)
        return new_signal

    def windowBasedSD(self, sig):
        signal = list(sig)
        new_signal = []
        for i in range(0, len(signal), 256):
            mean = self.find_mean(signal[i : i + 256])
            total = 0
            for j in range(i, i + 256):
                total += (signal[j] - mean) ** 2
            SD = (total / 256) ** (1/2)
            new_signal.append(SD)
        return new_signal

    def speechSegmentation(self, sig, threshold):
        signal = list(sig)
        for i in range(len(signal)):
            if signal[i] > threshold:
                signal[i] = 1
            else:
                signal[i] = 0
        return signal

    def XOR(self, a, b):
        return bool(a) != bool(b)

    def removeErrors(self, sig):
        signal = list(sig)
        errors = [[0, 1, 0], [0, 1, 1, 0]]
        for error in errors:
            for i in range(0, len(signal) - len(error) + 1):
                isError = True
                for j in range(len(error)):
                    if self.XOR(error[j], signal[i + j]) == 1:
                        isError = False
                if isError:
                    for j in range(len(error)):
                        signal[i + j] = 0
        return signal

    def speechReconstruction(self, sig, segmentedSignal):
        signal = list(sig)
        for i in range(len(segmentedSignal)):
            if segmentedSignal[i] == 0:
                for j in range(i * 256, i * 256 + 256):
                    signal[j] = 0
        return signal

    def get_window_size(self, file_name):
        spf = wave.open(file_name, 'r')
        return spf.getframerate() * 2

    def combineSignal(self, sig):
        signal = list(sig)
        new_signal = []
        for s in signal:
            if s != 0:
                new_signal.append(s)
        return new_signal

    def process(self, file_name, combine=False, threshold = 0.01):
        sample_rate, sig = wavfile.read(file_name)
        window_size = self.get_window_size(file_name)
        # Pre-processing
        new_signal = self.npToList(sig)
        new_signal = self.zero_mean(new_signal)
        new_signal = self.normalization(new_signal)
        new_signal = self.autoFixedLength(new_signal)

        # Segmentation
        segmentedSignal = self.power(new_signal)
        segmentedSignal = self.windowBasedSD(segmentedSignal)
        segmentedSignal = self.speechSegmentation(segmentedSignal, threshold)
        segmentedSignal = self.removeErrors(segmentedSignal)

        # Reconstruction
        new_signal = self.speechReconstruction(new_signal, segmentedSignal)

        if combine:
            new_signal = self.combineSignal(new_signal)

        return sample_rate, np.array(new_signal)
