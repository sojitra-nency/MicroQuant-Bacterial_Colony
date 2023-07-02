# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from skimage import draw, morphology, transform, filters, feature, measure, color
import cv2


def cut(img, sigma=0.1, plate_width=40):
    im = img.copy()
    im = transform.resize(im, (550, 672))
    contour = feature.canny(im, sigma=sigma)
    blotmap = morphology.dilation(contour, selem=morphology.disk(3))
    radius = np.arange(210, 275, step=3)
    hough = transform.hough_circle(blotmap, radius=radius)
    plate_index = np.unravel_index(hough.argmax(), hough.shape)
    center = (plate_index[1], plate_index[2])
    radius = radius[plate_index[0]] - plate_width
    c = draw.disk(center, radius)
    mask = np.zeros_like(im)
    mask[c] = 1.
    blotmap = blotmap * mask
    return blotmap


def recognize(blotmap):
    label = measure.label(blotmap, connectivity=1)
    label = label.astype(np.int32)  # Convert labels to int32
    blur_map = filters.gaussian(blotmap, 2)
    peaks = feature.peak_local_max(blur_map, min_distance=2, labels=label, num_peaks_per_label=10)
    return peaks.shape[0], peaks




def graph(img, peaks, show=True, fname=None):
    im = img.copy()
    im = transform.resize(im, (550, 672))
    im = color.gray2rgb(im)

    fig, ax = plt.subplots(dpi=150)
    ax.imshow(im) 
    ax.scatter(peaks[:, 1], peaks[:, 0], s=20, linewidths=0.3)
    ax.text(75, 520, 'count: {}'.format(peaks.shape[0]), color='white')
    plt.axis('off')
    if show:
        plt.show()
    if fname:
        fig.savefig(fname)



if __name__ == '__main__':
    img = cv2.imread('0B3.Tif', cv2.IMREAD_GRAYSCALE) / 255.0
    plate = cut(img)
    num, dots = recognize(plate)
    graph(img, dots, fname='test.png')
    # graph(plate, dots)
    print(num)
