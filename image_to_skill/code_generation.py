from tqdm import tqdm
from image_to_skill.image_processor import ImageDetails

def generate_code(image_details: ImageDetails) -> str:
    code: str = ""

    print("-- Configuration --")
    mode: str = input("Mode: ")
    base_fo: float = float(input("Base forward offset: "))
    base_so: float = float(input("Base side offset: "))
    base_y: float = float(input("Base Y offset: "))
    if mode == "HR":
        foward_offset: float = base_fo
        side_offset: float = image_details.width * 0.2 / 2 + base_so
        y_offset: float = image_details.height * 0.2 + base_y
    elif mode == "VT":
        foward_offset: float = image_details.height * -0.2 / 2 + base_fo
        side_offset: float = image_details.width * 0.2 / 2 + base_so
        y_offset: float = base_y
    else:
        print("!: Invalid or blank mode, mode defaulted to HR.")
        foward_offset: float = base_fo
        side_offset: float = image_details.width * 0.2 / 2 + base_so
        y_offset: float = image_details.height * 0.2 + base_y
    print()

    print("-- Generating --")
    with tqdm(
        total = image_details.height * image_details.width,
        unit = "px",
    ) as pbar:
        code += "{}: \n  Skills: \n".format(image_details.name)
        for y_index, colors_at_y in enumerate(image_details.pixel_colors):
            for x_index, color_at_xy in enumerate(colors_at_y):
                if color_at_xy[3] == 0:
                    pbar.update(1)
                    continue
                code += "    - effect:particles{{amount=1;color={c};Size={s};forwardOffset={fo};sideOffset={so};yOffset={y}}}\n".format(
                    c = "#{0:02x}{1:02x}{2:02x}".format(color_at_xy[0], color_at_xy[1], color_at_xy[2]),
                    # Number rounding is needed due to inaccuracy on floating point number calculations
                    s = round(color_at_xy[3] / 255, 3),
                    fo = round(foward_offset + y_index * 0.2, 3) if mode == "VT" else round(foward_offset, 3),
                    so = round(side_offset - x_index * 0.2, 3),
                    y = round(y_offset, 3) if mode == "VT" else round(y_offset - y_index * 0.2, 3)
                )
                pbar.update(1)

    return code