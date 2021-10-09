from os.path import basename
from typing import List, Tuple
from PIL import Image
from PIL.PyAccess import PyAccess

class ImageDetails:
    def __init__(self, name: str, width: int, height: int, pixel_colors: List[List[Tuple[int, int, int, int]]]) -> None:
        self.name: str = name
        self.width: int = width
        self.height: int = height
        self.pixel_colors: List[List[Tuple[int, int, int, int]]] = pixel_colors
    
    def __str__(self) -> str:
        return "ImageColorDetails{{width: {self.width}, height: {self.height}, pixel_colors: {self.pixel_colors}}}".format(self = self)

def get_color_details_from_image(img_path: str) -> ImageDetails:
    with Image.open(img_path).convert("RGBA") as im:
        color_access = im.load()
        return ImageDetails(
            name = basename(img_path), 
            width = im.size[0],
            height = im.size[1],
            pixel_colors = [[color_access[x, y] for x in range(im.size[0])] for y in range(im.size[1])]
        )