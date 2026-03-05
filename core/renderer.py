import matplotlib.pyplot as plt
from skimage import transform, color
import config

def graph(img, peaks, show=True, fname=None):
    """
    Visualizes the detection results by overlaying markers on the original image.
    """
    im = img.copy()
    im = transform.resize(im, config.TARGET_RESOLUTION)
    im = color.gray2rgb(im)

    fig, ax = plt.subplots(dpi=150)
    ax.imshow(im) 
    
    # Plot detected colonies
    ax.scatter(peaks[:, 1], peaks[:, 0], s=20, linewidths=0.3, edgecolors='red', facecolors='none')
    
    # Add count text
    ax.text(75, 520, f'Count: {peaks.shape[0]}', color='white', fontsize=12, fontweight='bold')
    
    plt.axis('off')
    
    if show:
        plt.show()
    
    if fname:
        fig.savefig(fname, bbox_inches='tight', pad_inches=0)
        plt.close(fig) # Close figure to free memory during batch processing
