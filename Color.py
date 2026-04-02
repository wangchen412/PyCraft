import Blocks
from scipy.spatial import KDTree
import numpy as np
import colorsys

names = list(Blocks.MC_BLOCK_MAP.keys())
rgbs = np.array(list(Blocks.MC_BLOCK_MAP.values()))
tree = KDTree(rgbs)

def find_best_block(rgb):
    _, index = tree.query(rgb)
    return names[index]

def coords_to_rgb(x, y):
    r, g, b = colorsys.hsv_to_rgb(x, y, 1.0)
    return (r * 255, g * 255, b * 255)