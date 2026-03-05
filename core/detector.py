import numpy as np
from skimage import draw, morphology, transform, feature, measure, filters
import config

def cut(img, sigma=config.CANNY_SIGMA, plate_width=config.PLATE_WIDTH_OFFSET):
    """
    Identifies the petri dish and masks out extraneous information.
    """
    im = img.copy()
    im = transform.resize(im, config.TARGET_RESOLUTION)
    
    # Edge detection
    contour = feature.canny(im, sigma=sigma)
    
    # Thicken edges for better circle detection
    blotmap = morphology.dilation(contour, footprint=morphology.disk(3))
    
    # Hough circle detection
    radius_range = np.arange(210, 275, step=3)
    hough = transform.hough_circle(blotmap, radius=radius_range)
    
    # Get the best fit circle
    plate_index = np.unravel_index(hough.argmax(), hough.shape)
    center = (plate_index[1], plate_index[2])
    radius = radius_range[plate_index[0]] - plate_width
    
    # Create mask
    c = draw.disk(center, radius)
    mask = np.zeros_like(im)
    mask[c] = 1.
    
    return blotmap * mask

def recognize(blotmap):
    """
    Identifies and counts individual bacterial colonies.
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
