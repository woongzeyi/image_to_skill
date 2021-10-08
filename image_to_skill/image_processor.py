from typing import List
from PIL import Image
from PIL.PyAccess import PyAccess

class ImageColorDetails:
    def __init__(self, width: int, height: int, pixel_colors: List[PyAccess]) -> None:
        self.width: int = width
        self.height: int = height
        self.pixel_colors: List[PyAccess] = pixel_colors
    
    def __str__(self) -> str:
        return "ImageColorDetails{{width: {self.width}, height: {self.height}, pixel_colors: {color_list}}}".format(
            self = self, 
            # color_list = [self.pixel_colors[x, y] for x in range(self.width) for y in range(self.height)]
            color_list = [[self.pixel_colors[x, y] for x in range(self.width)] for y in range(self.height)]
        )

def get_color_details_from_image(img_path: str) -> ImageColorDetails:
    with Image.open(img_path) as im:
        return ImageColorDetails(
            width = im.size[0],
            height = im.size[1],
            pixel_colors = im.load()
        )