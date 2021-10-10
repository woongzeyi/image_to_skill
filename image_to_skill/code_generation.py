from filetype.types import image
from image_to_skill.image_processor import ImageDetails
from os.path import splitext

def generate_code(image_details: ImageDetails) -> str:
    code = ""
    side_offset = image_details.width * 0.2 / 2
    y_offset = image_details.height * 0.2


    code += "{}: \n  Skills: \n".format(splitext(image_details.name)[0])
    for y_index, colors_at_y in enumerate(image_details.pixel_colors):
        for x_index, color_at_xy in enumerate(colors_at_y):
            if color_at_xy[3] < 255:
                continue
            code += "    - effect:particles{{a=1;c={c};forwardOffset=-1;sideOffset={so};y={y}}}\n".format(
                c = "#{0:02x}{1:02x}{2:02x}".format(color_at_xy[0], color_at_xy[1], color_at_xy[2]),
                # Number rounding is needed due to inaccuracy on floating point number calculations
                so = round(side_offset - x_index * 0.2, 1),
                y = round(y_offset - y_index * 0.2, 1)
            )

    return code