"""
Dependencies: Pillow, numpy
Instructions!

To encode:
encode_to_color("Your string here")

Optional params-
tilesize: Size of each square in the mosaic (in pixels). Default 5.
tiles_per_row: Number of squares per horizontal row of the mosaic. Default 10.
out_path: System path and name where you want your image to save. Default "image.png"


To decode:
decode_from_color("path\to\image.ext")

Returns string containing decoded message.

Optional params-
tilesize: Mosaic square size of your input image (in pixels). If this is wrong, it will translate incorrectly. Default 5.

"""

from PIL import Image,ImageDraw
import numpy as np

def cypher(in_string):
    # Encodes data to numpy array of RGB colors
    length = int(len(in_string))

    excess = length % 3
    if excess != 0:
        length += (3-excess)

    out = np.zeros((int(length/3),3))

    for e,char in enumerate(in_string):
        out[int(e/3),e%3] = ord(char)*2

    return out.astype("int")


def decypher(in_ndarray):
    # Decodes numpy array of RGB colors
    data = in_ndarray.flatten()

    out = []
    for char in data:
        out.append(chr(int(char/2)))

    return "".join(out)

def encode_to_color(in_string,tilesize=5,tiles_per_row=10,out_path="image.png"):
    length = len(in_string)
    excess = length % tiles_per_row
    if excess != 0:
        length += tiles_per_row - excess
    im_width = tiles_per_row * tilesize
    im_height = (int((length/3)/tiles_per_row) * tilesize)
    if (len(in_string)/3) % tiles_per_row != 0 and (len(in_string)/3) > tiles_per_row:
        im_height += tilesize

    im = Image.new("RGB",(im_width,im_height),"black")

    cyphered_data = cypher(in_string)
    draw = ImageDraw.Draw(im)
    for e,color in enumerate(cyphered_data):
        col = int(e/tiles_per_row)
        row = e % tiles_per_row
        draw.rectangle((row*tilesize,col*tilesize,(row*tilesize)+(tilesize-1),(col*tilesize)+(tilesize-1)),fill=(color[0],color[1],color[2]))

    im.save(out_path)
    print("Image saved to "+out_path)


def decode_from_color(in_image_path,tilesize=5):
    im = Image.open(in_image_path)
    tile_rows = int(im.width / tilesize)
    tile_cols = int(im.height / tilesize)

    colors = []
    for y in range(tile_cols):
        for x in range(tile_rows):
            color = im.getpixel((x*tilesize,y*tilesize))
            colors.append(color)

    return decypher(np.asarray(colors))
