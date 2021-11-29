"""A module for generating particle code files. """

from typing import List
from tqdm import tqdm
from image_to_skill.image_processor import ImageDetails

KNOWN_PARTICLE_TYPES: List[str] = [
    "barrier",
    "block_crack",
    "bubble",
    "bubble_column",
    "bubble_pop",
    "cloud",
    "crimson_spore",
    "crit",
    "crit_magic",
    "current_down",
    "damage_indicator",
    "dolphin",
    "dragon_breath",
    "drip_lava",
    "dripping_obsidian_tear",
    "drip_water",
    "enchantment_table",
    "end_rod",
    "explosion_normal",
    "explosion_huge",
    "explosion_large",
    "falling_dust",
    "falling_obsidian_tear",
    "fireworks_spark",
    "flame",
    "footstep",
    "heart",
    "item_crack",
    "landing_obsidian_tear",
    "lava",
    "mob_appearance",
    "nautilus",
    "note",
    "portal",
    "redstone",
    "slime",
    "smoke_large",
    "smoke_normal",
    "snowball",
    "snow_shovel",
    "soul",
    "soul_fire_flame",
    "spell_instant",
    "spell_mob",
    "spell_mob_ambient",
    "spell_witch",
    "splash",
    "squid_ink",
    "suspended",
    "suspended_depth",
    "sweep_attack",
    "town_aura",
    "villager_angry",
    "villager_happy",
    "wake",
    "warped_spore",
]


def generate_code(image_details: ImageDetails) -> str:
    """Takes in an ImageDetails object and returns a string of code generated from it"""

    code: str = ""

    # getting config values
    print("-- Configuration --")
    mode: str = input("Mode: ")
    particle_type: str = input("Particle type: ")
    particle_interval: float = float(input("Particle interval: "))
    particle_size: float = float(input("Particle size: "))
    base_fo: float = float(input("Base forward offset: "))
    base_so: float = float(input("Base side offset: "))
    base_y: float = float(input("Base Y offset: "))

    # particle_type check
    if particle_type not in KNOWN_PARTICLE_TYPES:
        print("!: Invalid or blank particle type, particle type defaulted to redstone.")
        particle_type = "redstone"

    # foward_offset, side_offset, y_offset calculation
    if mode == "HR":
        foward_offset: float = base_fo
        side_offset: float = image_details.width * particle_interval / 2 + base_so
        y_offset: float = image_details.height * particle_interval + base_y
    elif mode == "VT":
        foward_offset: float = image_details.height * -particle_interval / 2 + base_fo
        side_offset: float = image_details.width * particle_interval / 2 + base_so
        y_offset: float = base_y
    else:
        print("!: Invalid or blank mode, mode defaulted to HR.")
        foward_offset: float = base_fo
        side_offset: float = image_details.width * particle_interval / 2 + base_so
        y_offset: float = image_details.height * particle_interval + base_y
    print()

    # generating code with progress bar
    print("-- Generating --")
    with tqdm(
        total=image_details.height * image_details.width,
        unit="px",
    ) as pbar:
        code += f"{image_details.name}: \n  Skills: \n"
        for y_index, colors_at_y in enumerate(image_details.pixel_colors):
            for x_index, color_at_xy in enumerate(colors_at_y):
                if color_at_xy[3] == 0:
                    pbar.update(1)
                    continue
                # pylint: disable-next=C0209,C0301
                code += "    - effect:particles{{particle={p};amount=1;color={c};Size={s};forwardOffset={fo};sideOffset={so};yOffset={y}}}\n".format(
                    p=particle_type,
                    c="#{0:02x}{1:02x}{2:02x}".format(  # pylint: disable=C0209
                        color_at_xy[0],
                        color_at_xy[1],
                        color_at_xy[2]
                    ),
                    # Number rounding is needed due to inaccuracy on floating point number
                    # calculations
                    s=round(color_at_xy[3] / 255 * particle_size, 3),
                    fo=round(foward_offset + y_index * particle_interval, 3) if mode == "VT" \
                    else round(foward_offset, 3),
                    so=round(side_offset - x_index * particle_interval, 3),
                    y=round(y_offset, 3) if mode == "VT" \
                    else round(y_offset - y_index * particle_interval, 3)
                )
                pbar.update(1)

    return code
