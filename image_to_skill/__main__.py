import os
from os.path import isfile, join
from typing import Dict, List
from filetype import is_image
from filetype.types import image
from .image_processor import ImageColorDetails, get_color_details_from_image
from .code_generation import generate_code

def main():
    # Images need to be put into the `./images` directory
    images_directory: str = os.getcwd() + "\\images"
    os.makedirs(images_directory, exist_ok = True)

    # Opening a non-image file with PIL will throw an exception
    images: List[str] = [f 
        for f in os.listdir(images_directory) 
        if isfile(join(images_directory, f)) 
        if is_image(join(images_directory, f))
    ]

    image_to_colors: Dict[str, ImageColorDetails] = {}
    for i in images:
        image_to_colors[i] = get_color_details_from_image(join(images_directory, i))

    image_to_code: Dict[str, str] = {}
    for key, value in image_to_colors.items():
        image_to_code[key] = generate_code(value)
    print(image_to_code)

if __name__ == "__main__":
    main()