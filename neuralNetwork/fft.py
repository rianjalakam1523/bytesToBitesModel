import numpy as np
import scipy.fft as fft
import os

# AUTHOR: RIAN JALAKAM

class FFTDataPreprocessor:
    def __init__(self, data_dir: str, output_dir: str):
        self.data_dir = data_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def apply_1d_fft(self, signal_data: np.ndarray) -> np.ndarray:
        """
        Applies a 1D Fast Fourier Transform to convert time-domain 
        signals into frequency-domain representations.
        """
        fft_transformed = fft.fft(signal_data)
        magnitude_spectrum = np.abs(fft_transformed)
        return magnitude_spectrum

    def apply_2d_fft_image(self, image_data: np.ndarray) -> np.ndarray:
        """
        Applies a 2D Fast Fourier Transform for spatial frequency filtering 
        or edge enhancement in image datasets.
        """
        f_transform = fft.fft2(image_data)
        f_shifted = fft.fftshift(f_transform)
        magnitude_spectrum = 20 * np.log(np.abs(f_shifted) + 1)
        return magnitude_spectrum

    def process_batch(self, batch_data: np.ndarray, is_2d: bool = True) -> np.ndarray:
        """
        Batch processing wrapper to optimize throughput.
        """
        processed = []
        for item in batch_data:
            if is_2d:
                processed.append(self.apply_2d_fft_image(item))
            else:
                processed.append(self.apply_1d_fft(item))
        return np.array(processed)
