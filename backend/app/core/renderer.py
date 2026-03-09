import matplotlib.pyplot as plt
from skimage import transform, color
import numpy as np
from typing import Optional
from app.config import settings as config

class ColonyRenderer:
    """
    Handles visualization and graphical output for colony detection results.
    """

    @staticmethod
    def graph(img: np.ndarray, peaks: np.ndarray, show: bool = True, fname: Optional[str] = None):
        """
        Visualizes the detection results by overlaying markers on the original image.

        Args:
            img (np.ndarray): The original input image.
            peaks (np.ndarray): Coordinates of detected colonies.
            show (bool): Whether to display the plot interactively.
            fname (str, optional): File path to save the resulting image.
        """
        im = img.copy()
        im = transform.resize(im, config.TARGET_RESOLUTION)
        im = color.gray2rgb(im)

        fig, ax = plt.subplots(dpi=150)
        ax.imshow(im) 
        
        # Plot detected colonies
        # Using red circles for high visibility
        if peaks.size > 0:
            ax.scatter(peaks[:, 1], peaks[:, 0], s=20, linewidths=0.3, edgecolors='red', facecolors='none')
        
        # Add metadata text
        ax.text(
            75, 520, 
            f'Colony Count: {peaks.shape[0]}', 
            color='white', 
            fontsize=12, 
            fontweight='bold',
            bbox=dict(facecolor='black', alpha=0.5, edgecolor='none')
        )
        
        plt.axis('off')
        
        if show:
            plt.show()
        
        if fname:
            fig.savefig(fname, bbox_inches='tight', pad_inches=0)
            plt.close(fig) # Prevent memory leaks during batch runs
