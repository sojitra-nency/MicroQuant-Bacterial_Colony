import io
import base64

import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from skimage import transform, color

from app.core import ColonyDetector, ColonyRenderer
from app.config import settings
from app.models.schemas import AnalysisResponse, ColonyCoordinate

matplotlib.use("Agg")  # Non-interactive backend for server use


class AnalysisService:
    def __init__(self):
        self.detector = ColonyDetector()

    def analyze(self, image_bytes: bytes) -> AnalysisResponse:
        # Decode image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Could not decode image. Ensure it is a valid image file.")

        img = img / 255.0

        # Run detection pipeline
        plate_edges = self.detector.cut(img)
        count, peaks = self.detector.recognize(plate_edges)

        # Render annotated image to base64
        result_image = self._render_to_base64(img, peaks)

        coordinates = [ColonyCoordinate(x=int(p[1]), y=int(p[0])) for p in peaks]

        return AnalysisResponse(
            colony_count=count,
            coordinates=coordinates,
            result_image=result_image,
        )

    def _render_to_base64(self, img: np.ndarray, peaks: np.ndarray) -> str:
        im = img.copy()
        im = transform.resize(im, settings.TARGET_RESOLUTION)
        im = color.gray2rgb(im)

        fig, ax = plt.subplots(dpi=150)
        ax.imshow(im)

        if peaks.size > 0:
            ax.scatter(
                peaks[:, 1], peaks[:, 0],
                s=20, linewidths=0.3,
                edgecolors="red", facecolors="none",
            )

        ax.text(
            75, 520,
            f"Colony Count: {peaks.shape[0]}",
            color="white", fontsize=12, fontweight="bold",
            bbox=dict(facecolor="black", alpha=0.5, edgecolor="none"),
        )

        plt.axis("off")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        buf.seek(0)

        return base64.b64encode(buf.read()).decode("utf-8")
