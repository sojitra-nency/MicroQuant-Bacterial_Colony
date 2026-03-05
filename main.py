import os
import cv2
from core import cut, recognize, graph
import config

def process_directory(input_path=config.DEFAULT_INPUT_DIR, output_path=config.DEFAULT_OUTPUT_DIR):
    """
    Batch processes all images in a directory.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
        print(f"Created output directory: {output_path}")

    # Supported extensions
    valid_extensions = ('.tif', '.tiff', '.png', '.jpg', '.jpeg')
    files = [f for f in os.listdir(input_path) if f.lower().endswith(valid_extensions)]
    
    if not files:
        print(f"No valid images found in {input_path}")
        return

    print(f"Found {len(files)} images. Starting processing...")

    for file in files:
        input_file_path = os.path.join(input_path, file)
        output_file_name = f"{os.path.splitext(file)[0]}_count.png"
        output_file_path = os.path.join(output_path, output_file_name)

        try:
            # Load image
            img = cv2.imread(input_file_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Error: Could not read {file}")
                continue
            
            img = img / 255.0  # Normalize

            # Algorithm pipeline
            plate_edges = cut(img)
            count, coordinates = recognize(plate_edges)

            # Save result
            graph(img, coordinates, show=False, fname=output_file_path)
            
            print(f"Processed {file: <20} | Count: {count: >3}")

        except Exception as e:
            print(f"Failed to process {file}: {str(e)}")

    print("\nBatch processing complete.")

if __name__ == '__main__':
    # You can change the input/output paths here
    process_directory()
