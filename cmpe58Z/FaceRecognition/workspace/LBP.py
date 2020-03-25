import numpy as np
from PIL import Image


def lbp_cell_value(image_array, row ,column):
    val = 0
    threshold = image_array[row][column]
    if image_array[row-1][column-1] >= threshold : val |= (1<<0) # upper left
    if image_array[row-1][column] >= threshold : val |= (1<<1) # up
    if image_array[row-1][column+1] >= threshold : val |= (1<<2) # upper right
        
    if image_array[row][column+1] >= threshold : val |= (1<<3) # right
        
    if image_array[row+1][column+1] >= threshold : val |= (1<<4) # lower right
    if image_array[row+1][column] >= threshold : val |= (1<<5) # down
    if image_array[row+1][column-1] >= threshold : val |= (1<<6) # lower left
        
    if image_array[row][column-1] >= threshold : val |= (1<<7) # left
    return val

def to_LBP(pil_image):
    gray_scale_image = pil_image.convert(mode='L')
    image_array = np.asarray(gray_scale_image)
    height, width = image_array.shape
    lbp_array = np.zeros(shape=(height, width), dtype=np.int16)
    # TODO think about borders, they remain zeros for now
    for row_num in range(1, height-1):
        for column_num in range(1, width-1):
            lbp_array[row_num][column_num] = lbp_cell_value(image_array, row_num, column_num)

    lbp_image = Image.fromarray(lbp_array)
    return lbp_image
