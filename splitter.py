import os
import shutil
import numpy as np

def split_data(source_dir, train_dir, val_dir, test_dir, train_size=0.8, val_size=0.1):
    classes = os.listdir(source_dir)
    for cls in classes:
        # Create directories
        os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
        os.makedirs(os.path.join(val_dir, cls), exist_ok=True)
        os.makedirs(os.path.join(test_dir, cls), exist_ok=True)

        # Get files and shuffle
        files = os.listdir(os.path.join(source_dir, cls))
        np.random.shuffle(files)

        # Split files
        train_end = int(len(files) * train_size)
        val_end = int(len(files) * (train_size + val_size))
        train_files = files[:train_end]
        val_files = files[train_end:val_end]
        test_files = files[val_end:]

        # Copy files
        for f in train_files:
            shutil.copy(os.path.join(source_dir, cls, f), os.path.join(train_dir, cls))
        for f in val_files:
            shutil.copy(os.path.join(source_dir, cls, f), os.path.join(val_dir, cls))
        for f in test_files:
            shutil.copy(os.path.join(source_dir, cls, f), os.path.join(test_dir, cls))

# Example usage
source_dir = "/Users/aaryanpotdar/Desktop/Personal_Projects/TomatoDiseaseClassification/plant_data"
train_dir = "/Users/aaryanpotdar/Desktop/Personal_Projects/TomatoDiseaseClassification/dataset/train"
validation_dir = "/Users/aaryanpotdar/Desktop/Personal_Projects/TomatoDiseaseClassification/dataset/validation"
test_dir = "/Users/aaryanpotdar/Desktop/Personal_Projects/TomatoDiseaseClassification/dataset/test"

split_data(source_dir, train_dir, validation_dir, test_dir)
