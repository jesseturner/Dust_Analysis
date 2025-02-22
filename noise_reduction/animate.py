import os
import imageio
from PIL import Image

directory = "monthly_average"
starts_with = "2025_Jan"
ends_with = "_SWD_average.png"
png_files = [f for f in os.listdir(directory) if f.startswith(starts_with) and f.endswith(ends_with)]

png_files.sort()

images = []

for file in png_files:
    img_path = os.path.join(directory, file)
    img = Image.open(img_path)
    images.append(img)

output_file = starts_with+"_animation.gif"
images[0].save(output_file, save_all=True, append_images=images[1:], duration=500, loop=0)

print(f"Animation saved as {output_file}")