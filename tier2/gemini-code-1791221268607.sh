python -c "
import os
from PIL import Image

for f in os.listdir('.'):
    if f.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            im = Image.open(f)
            im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            im.save(f, optimize=True, quality=80)
            print('Optimized:', f)
        except Exception as e:
            pass
"