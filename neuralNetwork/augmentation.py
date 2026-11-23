import numpy as np

# AUTHOR: RIAN JALAKAM

class DataAugmenter:
    def __init__(self):
        pass

    def add_gaussian_noise(self, data: np.ndarray, mean: float = 0.0, std: float = 0.05) -> np.ndarray:
        """
        Adds random Gaussian noise to signals or images for robust feature learning.
        """
        noise = np.random.normal(mean, std, data.shape)
        return data + noise

    def random_horizontal_flip_2d(self, image: np.ndarray, p: float = 0.5) -> np.ndarray:
        """
        Applies a random horizontal flip to a 2D or 3D image array with probability p.
        """
        if np.random.rand() < p:
            return np.fliplr(image)
        return image

    def random_vertical_flip_2d(self, image: np.ndarray, p: float = 0.5) -> np.ndarray:
        """
        Applies a random vertical flip to a 2D or 3D image array with probability p.
        """
        if np.random.rand() < p:
            return np.flipud(image)
        return image

    def random_crop_2d(self, image: np.ndarray, crop_height: int, crop_width: int) -> np.ndarray:
        """
        Extracts a random spatial crop from an image array.
        """
        h, w = image.shape[0], image.shape[1]
        if crop_height > h or crop_width > w:
            raise ValueError("Crop dimensions exceed image dimensions.")
        
        start_h = np.random.randint(0, h - crop_height + 1)
        start_w = np.random.randint(0, w - crop_width + 1)
        
        if image.ndim == 3:
            return image[start_h:start_h + crop_height, start_w:start_w + crop_width, :]
        return image[start_h:start_h + crop_height, start_w:start_w + crop_width]

    def scale_intensity(self, data: np.ndarray, min_factor: float = 0.8, max_factor: float = 1.2) -> np.ndarray:
        """
        Scales the intensity values by a random factor to simulate lighting variations.
        """
        factor = np.random.uniform(min_factor, max_factor)
        return data * factor
