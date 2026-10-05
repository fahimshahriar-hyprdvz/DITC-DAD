#!/usr/bin/env python3
import os
import sys

# Auto-install Pillow image library if missing
try:
    from PIL import Image
except ImportError:
    print("Installing Pillow image processor...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image

# 500px is 4x retina sharpness for mobile grid thumbnails
MAX_DIMENSION = 500   
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')

def compress_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(IMAGE_EXTENSIONS) and not f.startswith('compress')]
    if not files:
        print(f"No image files found in '{folder_path}'.")
        return

    print(f"Found {len(files)} images. Compressing to max {MAX_DIMENSION}px...\n")
    
    total_before = 0
    total_after = 0
    processed = 0

    for idx, fname in enumerate(files, 1):
        fpath = os.path.join(folder_path, fname)
        size_before = os.path.getsize(fpath)
        total_before += size_before

        try:
            with Image.open(fpath) as img:
                # Resize proportionally using high-quality Lanczos resampling
                img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
                
                # Overwrite in-place to keep existing filenames completely intact
                ext = os.path.splitext(fname)[1].lower()
                if ext == '.png':
                    img.save(fpath, format='PNG', optimize=True)
                elif ext in ('.jpg', '.jpeg'):
                    img.save(fpath, format='JPEG', quality=75, optimize=True)
                elif ext == '.webp':
                    img.save(fpath, format='WEBP', quality=75)
                else:
                    img.save(fpath)

            size_after = os.path.getsize(fpath)
            total_after += size_after
            processed += 1
            savings = (1 - (size_after / size_before)) * 100 if size_before > 0 else 0
            print(f"[{processed}/{len(files)}] {fname}: {size_before // 1024} KB -> {size_after // 1024} KB ({savings:.0f}% smaller)")
        except Exception as e:
            print(f"[{processed}/{len(files)}] Error processing {fname}: {e}")

    saved_mb = (total_before - total_after) / (1024 * 1024)
    print("\n" + "="*50)
    print(f"COMPRESSION COMPLETE!")
    print(f"Processed:    {processed} images")
    print(f"Initial size: {total_before / (1024*1024):.1f} MB")
    print(f"Final size:   {total_after / (1024*1024):.1f} MB")
    print(f"Space saved:  {saved_mb:.1f} MB ({(1 - (total_after / total_before))*100:.1f}% reduction)")
    print("="*50)

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    compress_folder(target_dir)