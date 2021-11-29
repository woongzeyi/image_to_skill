"""A module for processing images into congestible data. """

from os.path import basename, splitext
from typing import List, Tuple
from PIL import Image


class ImageDetails:
    """A data class representing informations needed for basic code generation. """

    def __init__(self, name: str, width: int, height: int,
                 pixel_colors: List[List[Tuple[int, int, int, int]]]) -> None:
        self.name: str = name
        self.width: int = width
        self.height: int = height
        self.pixel_colors: List[List[Tuple[int, int, int, int]]] = pixel_colors


def get_color_details_from_image(img_path: str) -> ImageDetails:
    with Image.open(img_path).convert("RGBA") as image:
        color_access = image.load()
        return ImageDetails(
            name=splitext(basename(img_path))[0],
            width=image.size[0],
            height=image.size[1],
            pixel_colors=[
                [color_access[x, y] for x in range(image.size[0])] for y in range(image.size[1])
            ]
        )
