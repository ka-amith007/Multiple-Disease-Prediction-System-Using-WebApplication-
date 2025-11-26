"""
Logo Resizer for PWA
This script helps you create different sizes of your logo for mobile app installation
"""

from PIL import Image
import os

def resize_logo(input_path):
    """
    Resize logo to different sizes needed for PWA
    
    Args:
        input_path: Path to your original logo file
    """
    print("🎨 Logo Resizer for Mobile App")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"❌ Error: File not found: {input_path}")
        print("Please provide the correct path to your logo file")
        return
    
    try:
        # Open the image
        print(f"📂 Opening: {input_path}")
        img = Image.open(input_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            print("🔄 Converting to RGBA format...")
            img = img.convert('RGBA')
        
        # Create assets directory if it doesn't exist
        assets_dir = "assets"
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
            print(f"📁 Created {assets_dir} directory")
        
        # Sizes needed for PWA
        sizes = {
            'logo.png': (180, 180),
            'icon-192x192.png': (192, 192),
            'icon-512x512.png': (512, 512)
        }
        
        # Resize and save
        for filename, size in sizes.items():
            output_path = os.path.join(assets_dir, filename)
            print(f"✏️  Creating {size[0]}x{size[1]} version...")
            
            # Resize with high quality
            resized = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save
            resized.save(output_path, 'PNG', optimize=True)
            print(f"✅ Saved: {output_path}")
        
        print("\n" + "=" * 50)
        print("🎉 Success! All logo sizes created!")
        print(f"📁 Files saved in: {assets_dir}/")
        print("\n📱 Next steps:")
        print("1. Check the assets folder for your logo files")
        print("2. Deploy your app to Railway")
        print("3. Open the app on your phone and install it!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error processing image: {str(e)}")
        print("Make sure your file is a valid image (PNG, JPG, etc.)")


if __name__ == "__main__":
    print("\n")
    logo_path = input("Enter the path to your logo file: ").strip('"').strip("'")
    
    if logo_path:
        resize_logo(logo_path)
    else:
        print("❌ No file path provided!")
        print("\nUsage:")
        print('python resize_logo.py')
        print('Then enter: C:\\path\\to\\your\\logo.png')
