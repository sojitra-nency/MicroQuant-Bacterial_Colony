import numpy as np
from skimage import draw, morphology, transform, feature, measure, filters
from typing import Tuple, List, Optional
import config

class ColonyDetector:
    """
    Handles the image processing pipeline for isolating petri dishes 
    and identifying bacterial colonies.
    """

    def __init__(self, sigma: float = config.CANNY_SIGMA):
        """
        Initializes the detector with a specific sensitivity.

        Args:
            sigma (float): Sigma for Canny edge detection.
        """
        self.sigma = sigma

    def cut(self, img: np.ndarray, plate_width_offset: int = config.PLATE_WIDTH_OFFSET) -> np.ndarray:
        """
        Identifies the petri dish boundary and masks everything outside it.

        Args:
            img (np.ndarray): Normalized grayscale image (0.0 - 1.0).
            plate_width_offset (int): Padding to exclude the dish rim.

        Returns:
            np.ndarray: Binary edge map restricted to the inside of the dish.
        """
        im = img.copy()
        im = transform.resize(im, config.TARGET_RESOLUTION)
        
        # Edge detection
        contour = feature.canny(im, sigma=self.sigma)
        
        # Thicken edges for better circle detection
        blotmap = morphology.dilation(contour, footprint=morphology.disk(3))
        
        # Hough circle detection
        radius_range = np.arange(210, 275, step=3)
        hough = transform.hough_circle(blotmap, radius=radius_range)
        
        # Get the best fit circle
        plate_index = np.unravel_index(hough.argmax(), hough.shape)
        center = (plate_index[1], plate_index[2])
        radius = radius_range[plate_index[0]] - plate_width_offset
        
        # Create circular mask
        c = draw.disk(center, radius)
        mask = np.zeros_like(im)
        mask[c] = 1.
        
        return blotmap * mask

    def recognize(self, blotmap: np.ndarray) -> Tuple[int, np.ndarray]:
        """
        Labels connected segments and locates colony centers.

        Args:
            blotmap (np.ndarray): Masked edge map from cut().

        Returns:
            Tuple[int, np.ndarray]: (Total count, Array of peak coordinates).
        """
        # Label distinct regions
        label = measure.label(blotmap, connectivity=1).astype(np.int32)
        
        # Smooth to find peaks more accurately
        blur_map = filters.gaussian(blotmap, config.GAUSSIAN_SIGMA)
        
        # Locate local maxima
        peaks = feature.peak_local_max(
            blur_map, 
            min_distance=config.MIN_PEAK_DISTANCE, 
            labels=label, 
            num_peaks_per_label=config.MAX_PEAKS_PER_LABEL
        )
        
        return peaks.shape[0], peaks
