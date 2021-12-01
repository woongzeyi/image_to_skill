"""The module where the main entry point of the program lives. """

from os import makedirs, listdir, getcwd
from os.path import isfile, join, splitext
from typing import List
from filetype import is_image
from .image_processor import ImageDetails
from .code_generation import CodeGenerator, Mode, ParticleType


def main():
    """The main entry point of the program. """

    # Images need to be put into the `./images` directory
    images_directory: str = getcwd() + "\\images"
    makedirs(images_directory, exist_ok=True)

    # Opening a non-image file with PIL will throw an exception
    images: List[str] = [
        f
        for f in listdir(images_directory)
        if isfile(join(images_directory, f))
        if is_image(join(images_directory, f))
    ]
    print(f"Images found: \n{images}\n")

    if images:
        for i in images:
            print(f"<< {i} >>")
            with open(
                join(images_directory, splitext(i)[0] + ".yml"),
                'w',
                encoding="utf-8"
            ) as yaml_file:
                generator = CodeGenerator(
                    mode=Mode(input("Mode: ")),
                    particle_type=ParticleType(input("Particle type: ")),
                    particle_interval=float(input("Particle interval: ")),
                    particle_size=float(input("Particle size: ")),
                    base_forward_offset=float(input("Base forward offset: ")),
                    base_side_offset=float(input("Base side offset: ")),
                    base_y_offset=float(input("Base Y offset: ")),
                    image=ImageDetails.from_path(join(images_directory, i))
                )
                for line in generator.generate_code():
                    yaml_file.write(line)
    else:
        print("Execution ended due to no image found.")


if __name__ == "__main__":
    main()
