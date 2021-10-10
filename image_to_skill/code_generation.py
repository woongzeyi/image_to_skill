from filetype.types import image
from image_to_skill.image_processor import ImageDetails

def generate_code(image_details: ImageDetails) -> str:
    code: str = ""

    mode: str = image_details.name.split("_")[0]
    if mode == "IF":
        foward_offset: float = 1
        side_offset: float = image_details.width * 0.2 / 2
        y_offset: float = image_details.height * 0.2
    elif mode == "BH":
        foward_offset: float = -1
        side_offset: float = image_details.width * 0.2 / 2
        y_offset: float = image_details.height * 0.2
    elif mode == "AB":
        foward_offset: float = 0
        side_offset: float = image_details.width * 0.2 / 2
        y_offset: float = image_details.height * 0.2 + 2
    elif mode == "OF":
        foward_offset: float = image_details.height * -0.2 / 2
        side_offset: float = image_details.width * 0.2 / 2
        y_offset: float = 0
    else:
        foward_offset: float = 1
        side_offset: float = image_details.width * 0.2 / 2
        y_offset: float = image_details.height * 0.2
    


    code += "{}: \n  Skills: \n".format(image_details.name)
    for y_index, colors_at_y in enumerate(image_details.pixel_colors):
        for x_index, color_at_xy in enumerate(colors_at_y):
            if color_at_xy[3] == 0:
                continue
            code += "    - effect:particles{{amount=1;color={c};Size={s};forwardOffset={fo};sideOffset={so};yOffset={y}}}\n".format(
                c = "#{0:02x}{1:02x}{2:02x}".format(color_at_xy[0], color_at_xy[1], color_at_xy[2]),
                # Number rounding is needed due to inaccuracy on floating point number calculations
                s = round(color_at_xy[3] / 255, 3),
                fo = round(foward_offset + y_index * 0.2, 3) if mode == "OF" else round(foward_offset, 3),
                so = round(side_offset - x_index * 0.2, 3),
                y = round(y_offset, 3) if mode == "OF" else round(y_offset - y_index * 0.2, 3)
            )

    return code