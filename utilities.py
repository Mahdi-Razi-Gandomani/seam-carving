import numpy as np
import math
from typing import List


# Energy function
def DualGradientEnergy(image):
    H, W = image.shape[:2]
    energy = np.zeros((H, W), dtype=float)
    BORDER = 1000.0
    energy[0, :] = BORDER
    energy[-1, :] = BORDER
    energy[:, 0] = BORDER
    energy[:, -1] = BORDER
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            dx_sq = 0.0
            dy_sq = 0.0
            for c in range(image.shape[2]):
                rx = float(image[y, x + 1, c]) - float(image[y, x - 1, c])
                ry = float(image[y + 1, x, c]) - float(image[y - 1, x, c])
                dx_sq += rx * rx
                dy_sq += ry * ry
            energy[y, x] = math.sqrt(dx_sq + dy_sq)
    return energy


# Seam removal utilities
def remove_vertical_seam(image, seam):
    H, W = image.shape[:2]
    out = np.zeros((H, W - 1, image.shape[2]), dtype=image.dtype)
    for y in range(H):
        x = seam[y]
        out[y, :, :] = np.delete(image[y, :, :], x, axis=0)
    return out

def remove_horizontal_seam(image, seam):
    H, W = image.shape[:2]
    out = np.zeros((H - 1, W, image.shape[2]), dtype=image.dtype)
    for x in range(W):
        y = seam[x]
        out[:, x, :] = np.delete(image[:, x, :], y, axis=0)
    return out




# Seam insertion
def insert_vertical_seam(image, seam):
    H, W = image.shape[:2]
    out = np.zeros((H, W + 1, image.shape[2]), dtype=image.dtype)
    for y in range(H):
        x = int(seam[y])
        if x > 0:
            out[y, : x, :] = image[y, : x, :]
        # Duplicate the seam pixel
        if x < W - 1:
            out[y, x, :] = ((image[y, x, :].astype(float) + image[y, x + 1, :].astype(float)) / 2).astype(image.dtype)
            out[y, x + 1, :] = out[y,x, :]
        else:
            out[y, x, :] = image[y, x, :]
            out[y, x + 1, :] = image[y, x, :]
        
        if x + 1 < W:
            out[y, x + 2 :, :] = image[y, x + 1 :, :]
    return out


def insert_horizontal_seam(image, seam):
    H, W = image.shape[:2]
    out = np.zeros((H + 1, W, image.shape[2]), dtype=image.dtype)
    for x in range(W):
        y = int(seam[x])
        if y > 0:
            out[:y, x, :] = image[:y, x, :]
        if y < H - 1:
            out[y, x, :] = ((image[y, x, :].astype(float) + image[y + 1, x, :].astype(float)) / 2).astype(image.dtype)
            out[y + 1, x, :] = out[y, x, :]
        else:
            out[y, x, :] = image[y, x, :]
            out[y + 1, x, :] = image[y, x, :]
        if y + 1 < H:
            out[y + 2 :, x, :] = image[y + 1 :,x, :]
    return out

