from typing import List
from PIL import Image, ImageDraw


def draw_vertical_seam(image: Image.Image, seam: List[int], color=(255, 0, 0)) -> Image.Image:
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    for y, x in enumerate(seam):
        draw.point((x, y), fill=color)
    return img_copy

def draw_horizontal_seam(image: Image.Image, seam: List[int], color=(255, 0, 0)) -> Image.Image:
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    for x, y in enumerate(seam):
        draw.point((x, y), fill=color)
    return img_copy

#Utilities for GIF
def pad_to_size(img, target_size, color=(255, 255, 255)):
    W, H = target_size
    w, h = img.size
    new_img = Image.new("RGB", (W, H), color)
    left = (W - w) // 2
    top = (H - h) // 2
    new_img.paste(img, (left, top))
    return new_img


def save_gif(frames, gif_path, duration=100):
    # find max width and height across all frames
    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    frames_padded = [pad_to_size(f, (max_w, max_h)) for f in frames]
    frames_padded[0].save(
        gif_path,
        save_all=True,
        append_images=frames_padded[1:],
        duration=duration,
        loop=0
    )
    print(f"Saved GIF to {gif_path}")
