import os
import cv2

# Define the target size
target_size = (600, 800)

# Function to upscale an image using OpenCV
def upscale_image(image_path):
    try:
        image = cv2.imread(image_path)
        image = cv2.resize(image, target_size, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(image_path, image)
        print(f"Processed: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Recursively traverse directories
def process_directories(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower() == "cover.jpg":
                image_path = os.path.join(root, file)
                upscale_image(image_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directories(current_directory)
