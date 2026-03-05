# MicroQuant: Bacterial Colony Counter

A modular Python tool for automated detection and counting of bacterial colonies in petri dish images.

---

## 🚀 Overview
MicroQuant uses computer vision techniques (Circular Hough Transform, Canny Edge Detection, and Peak Local Maxima) to isolate petri dishes and count colonies with high accuracy.

## 🛠 Project Structure
```text
MicroQuant-Bacterial_Colony/
├── core/                   # Main processing logic
│   ├── detector.py         # Image segmentation & colony counting
│   └── renderer.py         # visualization & output generation
├── docs/                   # Full technical documentation
├── jerms/                  # Input image directory (example)
├── results/                # Processed output visualizations
├── config.py               # Global settings & sensitivity parameters
├── main.py                 # CLI Batch processing entry point
└── requirements.txt        # Dependencies
```

## 📦 Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `.\venv\Scripts\activate` on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Usage
1. Place your images in a folder (default: `jerms/`).
2. Run the batch processor:
   ```bash
   python main.py
   ```
3. Check the `results/` folder for visualized counts.

## 🤝 Contributing
Please read [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the modular architecture of the project.
