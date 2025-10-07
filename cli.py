import argparse
from PIL import Image
import numpy as np
from dijkstra import DijkstraMethod
from dynamic_programming import DpMethod
from utilities import DualGradientEnergy, remove_vertical_seam, remove_horizontal_seam
from visualization import draw_vertical_seam, draw_horizontal_seam, save_gif


def run_cli():
    parser = argparse.ArgumentParser(description="Seam carving utility")
    parser.add_argument("input", help="Input image file")
    parser.add_argument("output", help="Output image file")
    parser.add_argument("--vertical", type=int, default=0, help="Number of vertical seams to remove")
    parser.add_argument("--horizontal", type=int, default=0, help="Number of horizontal seams to remove")
    parser.add_argument("--method", choices=["dp", "dijkstra"], default="dp", help="Seam finding method")
    parser.add_argument("--gif", action="store_true", help="Save a GIF of the seam removal/insertion process")

    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")
    arr = np.array(img)
    finder = DpMethod() if args.method == "dp" else DijkstraMethod()
    frames = [img.copy()] if args.gif else []


    # Shrink vertical
    for _ in range(args.vertical):
        energy = DualGradientEnergy(arr)
        seam = finder.find_vertical_seam(energy)
        if args.gif:
            frames.append(draw_vertical_seam(Image.fromarray(arr), seam))
        arr = remove_vertical_seam(arr, seam)

    # Shrink horizontal
    for _ in range(args.horizontal):
        energy = DualGradientEnergy(arr)
        seam = finder.find_horizontal_seam(energy)
        if args.gif:
            frames.append(draw_horizontal_seam(Image.fromarray(arr), seam))
        arr = remove_horizontal_seam(arr, seam)


    # Save final image
    out_img = Image.fromarray(arr)
    out_img.save(args.output)
    print(f"Saved output image to {args.output}")

    if args.gif and len(frames) > 1:
        gif_file = args.output.replace(".jpg", "_process.gif").replace(".png", "_process.gif")
        save_gif(frames, gif_file)
