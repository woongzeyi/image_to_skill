from os import makedirs, listdir, getcwd
from os.path import isfile, join, splitext
from typing import List
from filetype import is_image
from .image_processor import get_color_details_from_image
from .code_generation import generate_code

def main():
    # Images need to be put into the `./images` directory
    images_directory: str = getcwd() + "\\images"
    makedirs(images_directory, exist_ok = True)

    # Opening a non-image file with PIL will throw an exception
    images: List[str] = [f 
        for f in listdir(images_directory) 
        if isfile(join(images_directory, f)) 
        if is_image(join(images_directory, f))
    ]
    print("Images found: \n{}".format(images), end = "")

    if images:
        for i in images:
            print("\n\n\n", end="")
            print("<< {} >>".format(i))
            with open(join(images_directory, splitext(i)[0] + ".yml"), 'w') as yaml_file:
                yaml_file.write(generate_code(get_color_details_from_image(join(images_directory, i))))
    else:
        print("Execution ended due to no image found.")
        
if __name__ == "__main__":
    main()