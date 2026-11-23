import numpy as np

# AUTHOR: RIAN JALAKAM

class DatasetNormalizer:
    def __init__(self):
        self.mean = None
        self.std = None
        self.min_val = None
        self.max_val = None

    def fit(self, data: np.ndarray) -> None:
        """
        Computes global mean and standard deviation across the dataset.
        """
        self.mean = np.mean(data, axis=0)
        self.std = np.std(data, axis=0)
        # Prevent division by zero for constant features
        self.std = np.where(self.std == 0.0, 1.0, self.std)

    def fit_min_max(self, data: np.ndarray) -> None:
        """
        Computes global minimum and maximum values across the dataset.
        """
        self.min_val = np.min(data, axis=0)
        self.max_val = np.max(data, axis=0)
        # Prevent division by zero if min equals max
        self.max_val = np.where(self.max_val == self.min_val, self.min_val + 1.0, self.max_val)

    def transform_z_score(self, data: np.ndarray) -> np.ndarray:
        """
        Applies standard score (Z-score) normalization: (x - mean) / std.
        """
        if self.mean is None or self.std is None:
            raise ValueError("Normalizer must be fitted before transformation.")
        return (data - self.mean) / self.std

    def transform_min_max(self, data: np.ndarray) -> np.ndarray:
        """
        Applies Min-Max scaling to map values between [0, 1].
        """
        if self.min_val is None or self.max_val is None:
            raise ValueError("Normalizer must be fitted before transformation.")
        return (data - self.min_val) / (self.max_val - self.min_val)

    def inverse_transform_z_score(self, scaled_data: np.ndarray) -> np.ndarray:
        """
        Reverses Z-score normalization back to original scale.
        """
        if self.mean is None or self.std is None:
            raise ValueError("Normalizer has not been fitted.")
        return (scaled_data * self.std) + self.mean
