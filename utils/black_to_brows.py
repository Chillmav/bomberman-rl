import numpy as np

def replace_black_with_brown(image_array):

    brown = [244, 164, 96]
    

    black_pixels = (image_array[:, :, 0] == 0) & (image_array[:, :, 1] == 0) & (image_array[:, :, 2] == 0)
    

    image_array[black_pixels] = brown
    return image_array