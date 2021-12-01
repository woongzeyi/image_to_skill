"""A module for processing images into congestible data. """

from os.path import basename, splitext
from dataclasses import dataclass
from PIL import Image


@dataclass
class ImageDetails:
    """A data class representing informations needed for basic code generation. """

    name: str
    width: int
    height: int
    pixel_access: "PixelAccess"

    @classmethod
    def from_path(cls, img_path: str) -> "ImageDetails":
        """Constructs an ImageDetails object from the image of img_path. """
        with Image.open(img_path).convert("RGBA") as image:
            return cls(
                name=splitext(basename(img_path))[0],
                width=image.size[0],
                height=image.size[1],
                pixel_access=image.load()
            )
