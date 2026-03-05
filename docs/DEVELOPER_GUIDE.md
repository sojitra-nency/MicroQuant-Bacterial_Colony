# Developer Guide & Project Documentation

Welcome to the MicroQuant documentation. This guide is intended for developers and contributors to understand the underlying architecture and how to extend the project.

## 🏗 Modular Architecture

The project is split into separate modules to ensure high maintainability:

### 1. `config.py` (Centralized Settings)
All "magic numbers" and thresholds are stored here. If the detection is too sensitive or not sensitive enough, developers should adjust `CANNY_SIGMA` or `MIN_PEAK_DISTANCE` in this file.

### 2. `core.detector` (The Algorithm)
This module handles the core computer vision pipeline:
- **`cut()`**: Uses Circular Hough Transform to find the largest circle (the plate) and masks outside noise.
- **`recognize()`**: Uses local peak detection to count dots.

### 3. `core.renderer` (Visual Proof)
Handles the Matplotlib logic to draw dots and text on images. It is decoupled from the algorithm, allowing for future web or GUI integrations.

## 🛠 Code Standards

- **Docstrings**: Every function must follow the Google style docstring format.
- **Typing**: Use Python type hints for better IDE support.
- **Classes**: Logic should be encapsulated in classes where it makes sense for state management.

## 🧪 How to Extend
- **Adding a new filter**: Add a method to `ColonyDetector` class in `detector.py`.
- **Changing Visualization**: Modify `ColonyRenderer` in `renderer.py`.

## 📈 Future Roadmap
- Integration of Deep Learning (YOLO/U-Net) for dense colony clusters.
- Development of a FastAPI-based web interface.
