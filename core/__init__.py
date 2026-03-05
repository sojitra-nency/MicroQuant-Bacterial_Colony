from .detector import ColonyDetector
from .renderer import ColonyRenderer

# Helper functions for backward compatibility or simple access
def cut(img, sigma=None):
    detector = ColonyDetector(sigma) if sigma else ColonyDetector()
    return detector.cut(img)

def recognize(blotmap):
    detector = ColonyDetector()
    return detector.recognize(blotmap)

def graph(img, peaks, show=True, fname=None):
    ColonyRenderer.graph(img, peaks, show, fname)

__all__ = ['ColonyDetector', 'ColonyRenderer', 'cut', 'recognize', 'graph']
