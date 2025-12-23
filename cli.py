import argparse
from PIL import Image
import numpy as np
from dijkstra import DijkstraMethod
from dynamic_programming import DpMethod
from utilities import DualGradientEnergy, remove_vertical_seam, remove_horizontal_seam, insert_vertical_seam, insert_horizontal_seam
from visualization import draw_vertical_seam, draw_horizontal_seam, save_gif


def run_cli():
    parser = argparse.ArgumentParser(description="Seam carving utility")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--vertical", type=int, default=0, help="positive=enlarge, negative=shrink")
    parser.add_argument("--horizontal", type=int, default=0, help="positive=enlarge, negative=shrink")
    parser.add_argument("--method", choices=["dp", "dijkstra"], default="dp")
    parser.add_argument("--gif", action="store_true", help="Save a GIF of the process")

    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")
    arr = np.array(img)
    finder = DpMethod() if args.method == "dp" else DijkstraMethod()
    frames = [img.copy()] if args.gif else []


    # vertical seams
    if args.vertical < 0:
        # Shrinks
        for _ in range(abs(args.vertical)):
            energy = DualGradientEnergy(arr)
            seam = finder.find_vertical_seam(energy)
            if args.gif:
                frames.append(draw_vertical_seam(Image.fromarray(arr), seam))
            arr = remove_vertical_seam(arr, seam)
    
    elif args.vertical > 0:
        # Enlarge
        sti = []
        tmp = arr.copy()
        for i in range(args.vertical):
            energy = DualGradientEnergy(tmp)
            seam = finder.find_vertical_seam(energy)
            sti.append(np.array(seam, dtype=int))
            tmp = remove_vertical_seam(tmp, seam)

        sorted = []
        for i, seam in enumerate(sti):
            adjusted = seam.copy()

            
            for j in range(i):
                for y in range(len(adjusted)):
                    if sti[j][y] <= seam[y]:
                        adjusted[y] += 1
            sorted.append(adjusted)
        
        # Insert them in order
        for seam in sorted:
            if args.gif:
                frames.append(draw_vertical_seam(Image.fromarray(arr), seam.tolist()))
            arr = insert_vertical_seam(arr, seam.tolist())


    
    # Horizontal seams
    if args.horizontal < 0:
        # Shrink
        for _ in range(abs(args.horizontal)):
            energy = DualGradientEnergy(arr)
            seam = finder.find_horizontal_seam(energy)
            if args.gif:
                frames.append(draw_horizontal_seam(Image.fromarray(arr), seam))
            arr = remove_horizontal_seam(arr, seam)
    
    elif args.horizontal > 0:
        # Enlarge
        sti = []
        tmp = arr.copy()
        for i in range(args.horizontal):
            energy = DualGradientEnergy(tmp)
            seam = finder.find_horizontal_seam(energy)
            sti.append(seam.copy())
            for j in range(len(sti)-1):
                for x in range(len(sti[j])):
                    if sti[j][x] >= seam[x]:
                        sti[j][x] += 1
            
            
            tmp = remove_horizontal_seam(tmp, seam)
        
        # Insert them in order
        for seam in sti:
            if args.gif:
                frames.append(draw_horizontal_seam(Image.fromarray(arr), seam))
            arr = insert_horizontal_seam(arr, seam)


    
    
    out_img = Image.fromarray(arr)
    out_img.save(args.output)
    print(f"Saved output image to {args.output}")

    if args.gif and len(frames) > 1:
        gif_file = args.output.replace(".jpg", "_process.gif").replace(".png", "_process.gif")
        save_gif(frames, gif_file)
