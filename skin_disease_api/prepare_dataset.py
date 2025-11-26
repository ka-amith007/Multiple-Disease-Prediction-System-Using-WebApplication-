"""
Dataset Preparation Script for Skin Disease Classification
Downloads and organizes skin disease images from Kaggle

DATASET SOURCES:
1. ISIC Archive (International Skin Imaging Collaboration) - Melanoma
2. DermNet NZ - Various skin diseases
3. Kaggle Skin Disease Dataset

INSTRUCTIONS:
1. Install kaggle: pip install kaggle
2. Set up Kaggle API credentials (~/.kaggle/kaggle.json)
3. Run this script: python prepare_dataset.py
"""

import os
import shutil
import random
from pathlib import Path

# Configuration
DATASET_ROOT = 'dataset'
TRAIN_DIR = os.path.join(DATASET_ROOT, 'train')
VAL_DIR = os.path.join(DATASET_ROOT, 'validation')
VALIDATION_SPLIT = 0.2

CLASSES = ['Acne', 'Eczema', 'Healthy', 'Melanoma', 'Psoriasis', 'Ringworm']

def create_directory_structure():
    """Create the directory structure for training and validation"""
    print("Creating directory structure...")
    
    for split in ['train', 'validation']:
        for cls in CLASSES:
            path = os.path.join(DATASET_ROOT, split, cls)
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")

def download_kaggle_datasets():
    """
    Download datasets from Kaggle
    
    To use this function:
    1. Install kaggle: pip install kaggle
    2. Get your API key from kaggle.com/account
    3. Place kaggle.json in ~/.kaggle/
    """
    print("\n" + "="*70)
    print("KAGGLE DATASET DOWNLOAD")
    print("="*70)
    
    try:
        import kaggle
        
        # Example datasets (replace with actual dataset names)
        datasets = [
            'kmader/skin-cancer-mnist-ham10000',  # Melanoma and other lesions
            'shubhamgoel27/dermnet',  # Various skin diseases
        ]
        
        print("\nDownloading datasets from Kaggle...")
        for dataset in datasets:
            try:
                print(f"\nDownloading: {dataset}")
                kaggle.api.dataset_download_files(
                    dataset,
                    path=os.path.join(DATASET_ROOT, 'raw'),
                    unzip=True
                )
                print(f"✓ Downloaded: {dataset}")
            except Exception as e:
                print(f"✗ Error downloading {dataset}: {str(e)}")
        
        print("\n✓ Dataset download completed!")
        
    except ImportError:
        print("\n⚠️  Kaggle API not installed.")
        print("Install it with: pip install kaggle")
        print("\nAlternatively, download datasets manually from:")
        print("1. https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000")
        print("2. https://www.kaggle.com/datasets/shubhamgoel27/dermnet")
        print("3. https://www.isic-archive.com/")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nTo use Kaggle API:")
        print("1. Get API key from https://www.kaggle.com/account")
        print("2. Place kaggle.json in ~/.kaggle/ (Unix) or C:\\Users\\<username>\\.kaggle\\ (Windows)")

def organize_dataset():
    """
    Organize downloaded images into class folders
    
    NOTE: This is a template function. You need to customize it based on
    the actual structure of your downloaded datasets.
    """
    print("\n" + "="*70)
    print("DATASET ORGANIZATION")
    print("="*70)
    print("\n⚠️  This function needs to be customized based on your dataset structure.")
    print("\nExpected manual organization:")
    print(f"Place images in: {DATASET_ROOT}/raw/[class_name]/")
    print(f"Classes: {', '.join(CLASSES)}")
    
    raw_path = os.path.join(DATASET_ROOT, 'raw')
    
    if not os.path.exists(raw_path):
        print(f"\n✗ Raw dataset directory not found: {raw_path}")
        print("Please download and extract datasets manually.")
        return
    
    # Check if raw data has been organized
    print("\nSearching for organized class folders...")
    for cls in CLASSES:
        cls_path = os.path.join(raw_path, cls)
        if os.path.exists(cls_path):
            images = [f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"Found {len(images)} images in {cls}/")

def split_dataset():
    """Split dataset into training and validation sets"""
    print("\n" + "="*70)
    print("SPLITTING DATASET")
    print("="*70)
    
    raw_path = os.path.join(DATASET_ROOT, 'raw')
    
    if not os.path.exists(raw_path):
        print(f"\n✗ Raw dataset directory not found: {raw_path}")
        return
    
    for cls in CLASSES:
        cls_raw_path = os.path.join(raw_path, cls)
        
        if not os.path.exists(cls_raw_path):
            print(f"\n⚠️  Class folder not found: {cls}")
            continue
        
        # Get all images
        images = [f for f in os.listdir(cls_raw_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        if not images:
            print(f"\n⚠️  No images found in {cls}/")
            continue
        
        # Shuffle images
        random.shuffle(images)
        
        # Split
        split_idx = int(len(images) * (1 - VALIDATION_SPLIT))
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        print(f"\n{cls}:")
        print(f"  Total: {len(images)}")
        print(f"  Train: {len(train_images)}")
        print(f"  Validation: {len(val_images)}")
        
        # Copy to train directory
        train_cls_path = os.path.join(TRAIN_DIR, cls)
        for img in train_images:
            src = os.path.join(cls_raw_path, img)
            dst = os.path.join(train_cls_path, img)
            shutil.copy2(src, dst)
        
        # Copy to validation directory
        val_cls_path = os.path.join(VAL_DIR, cls)
        for img in val_images:
            src = os.path.join(cls_raw_path, img)
            dst = os.path.join(val_cls_path, img)
            shutil.copy2(src, dst)
    
    print("\n✓ Dataset split completed!")

def verify_dataset():
    """Verify the dataset structure and count images"""
    print("\n" + "="*70)
    print("DATASET VERIFICATION")
    print("="*70)
    
    for split in ['train', 'validation']:
        split_path = os.path.join(DATASET_ROOT, split)
        print(f"\n{split.upper()} SET:")
        
        if not os.path.exists(split_path):
            print(f"  ✗ Directory not found: {split_path}")
            continue
        
        total = 0
        for cls in CLASSES:
            cls_path = os.path.join(split_path, cls)
            if os.path.exists(cls_path):
                count = len([f for f in os.listdir(cls_path) 
                           if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
                print(f"  {cls}: {count} images")
                total += count
            else:
                print(f"  {cls}: 0 images (folder not found)")
        
        print(f"  TOTAL: {total} images")

def create_sample_structure():
    """Create a sample structure guide for manual dataset organization"""
    print("\n" + "="*70)
    print("MANUAL DATASET ORGANIZATION GUIDE")
    print("="*70)
    
    guide = f"""
To manually organize your dataset:

1. Create this folder structure:
   {DATASET_ROOT}/
   └── raw/
       ├── Acne/
       ├── Eczema/
       ├── Healthy/
       ├── Melanoma/
       ├── Psoriasis/
       └── Ringworm/

2. Place images in respective folders:
   - Minimum 100 images per class recommended
   - Supported formats: .jpg, .jpeg, .png, .bmp
   - Image naming: anything.jpg (e.g., acne_001.jpg)

3. Dataset sources:
   - Kaggle: https://www.kaggle.com/datasets
   - ISIC Archive: https://www.isic-archive.com/
   - DermNet NZ: https://dermnetnz.org/
   - HAM10000: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000

4. After organizing, run this script again to split the dataset.

Current dataset structure should look like:
"""
    print(guide)
    
    # Create README
    with open(os.path.join(DATASET_ROOT, 'README.txt'), 'w') as f:
        f.write(guide)
    
    print(f"✓ Guide saved to: {DATASET_ROOT}/README.txt")

def main():
    """Main function to prepare the dataset"""
    print("\n" + "="*70)
    print("SKIN DISEASE DATASET PREPARATION")
    print("="*70)
    
    # Create directory structure
    create_directory_structure()
    
    # Create guide
    create_sample_structure()
    
    # Try to download from Kaggle
    response = input("\nDo you want to try downloading from Kaggle? (y/n): ")
    if response.lower() == 'y':
        download_kaggle_datasets()
    
    # Check if raw data exists
    raw_path = os.path.join(DATASET_ROOT, 'raw')
    if os.path.exists(raw_path):
        print("\n✓ Raw dataset folder found!")
        
        response = input("\nDo you want to split the dataset now? (y/n): ")
        if response.lower() == 'y':
            split_dataset()
            verify_dataset()
    else:
        print(f"\n⚠️  Please organize your images in: {raw_path}")
        print("Then run this script again to split the dataset.")
    
    print("\n" + "="*70)
    print("SETUP COMPLETED")
    print("="*70)
    print("\nNext steps:")
    print("1. Organize images in dataset/raw/[class_name]/")
    print("2. Run this script again to split dataset")
    print("3. Run train_model.py to train the model")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
