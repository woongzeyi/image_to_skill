"""A module for generating particle code files. """

from typing import Iterator
from dataclasses import dataclass, field
from enum import Enum
from image_to_skill.image_processor import ImageDetails


class Mode(Enum):
    """Modes for particle positioning. """
    HORIZONTAL = "HR"
    VERTICAL = "VT"


class ParticleType(Enum):
    """Available particle types for generated particles. """
    BARRIER = "barrier"
    BLOCK_CRACK = "block_crack"
    BUBBLE = "bubble"
    BUBBLE_COLUMN = "bubble_column"
    BUBBLE_POP = "bubble_pop"
    CLOUD = "cloud"
    CRIMSON_SPORE = "crimson_spore"
    CRIT = "crit"
    CRIT_MAGIC = "crit_magic"
    CURRENT_DOWN = "current_down"
    DAMAGE_INDICATOR = "damage_indicator"
    DOLPHIN = "dolphin"
    DRAGON_BREATH = "dragon_breath"
    DRIP_LAVA = "drip_lava"
    DRIPPING_OBSIDIAN_TEAR = "dripping_obsidian_tear"
    DRIP_WATER = "drip_water"
    ENCHANTMENT_TABLE = "enchantment_table"
    END_ROD = "end_rod"
    EXPLOSION_NORMAL = "explosion_normal"
    EXPLOSION_HUGE = "explosion_huge"
    EXPLOSION_LARGE = "explosion_large"
    FALLING_DUST = "falling_dust"
    FALLING_OBSIDIAN_TEAR = "falling_obsidian_tear"
    FIREWORKS_SPARK = "fireworks_spark"
    FLAME = "flame"
    FOOTSTEP = "footstep"
    HEART = "heart"
    ITEM_CRACK = "item_crack"
    LANDING_OBSIDIAN_TEAR = "landing_obsidian_tear"
    LAVA = "lava"
    MOB_APPEARANCE = "mob_appearance"
    NAUTILUS = "nautilus"
    NOTE = "note"
    PORTAL = "portal"
    REDSTONE = "redstone"
    SLIME = "slime"
    SMOKE_LARGE = "smoke_large"
    SMOKE_NORMAL = "smoke_normal"
    SNOWBALL = "snowball"
    SNOW_SHOVEL = "snow_shovel"
    SOUL = "soul"
    SOUL_FIRE_FLAME = "soul_fire_flame"
    SPELL_INSTANT = "spell_instant"
    SPELL_MOB = "spell_mob"
    SPELL_MOB_AMBIENT = "spell_mob_ambient"
    SPELL_WITCH = "spell_witch"
    SPLASH = "splash"
    SQUID_INK = "squid_ink"
    SUSPENDED = "suspended"
    SUSPENDED_DEPTH = "suspended_depth"
    SWEEP_ATTACK = "sweep_attack"
    TOWN_AURA = "town_aura"
    VILLAGER_ANGRY = "villager_angry"
    VILLAGER_HAPPY = "villager_happy"
    WAKE = "wake"
    WARPED_SPORE = "warped_spore"


@dataclass
# pylint: disable-next=R0902
class CodeGenerator:
    """A dataclass responsible for taking in its own required configuration and
    generating code from it.
    """

    mode: Mode
    particle_type: ParticleType
    particle_interval: float
    particle_size: float
    base_forward_offset: float
    base_side_offset: float
    base_y_offset: float
    image: ImageDetails

    forward_offset: float = field(init=False)
    side_offset: float = field(init=False)
    y_offset: float = field(init=False)

    def __post_init__(self):
        if self.mode is Mode.HORIZONTAL:
            self.foward_offset = self.base_forward_offset
            self.side_offset = self.image.width * self.particle_interval / 2 + self.base_side_offset
            self.y_offset = self.image.height * self.particle_interval + self.base_y_offset
        elif self.mode is Mode.VERTICAL:
            self.foward_offset = self.image.height * -self.particle_interval / 2 \
                + self.base_forward_offset
            self.side_offset = self.image.width * self.particle_interval / 2 \
                + self.base_forward_offset
            self.y_offset = self.base_y_offset

    def generate_code(self) -> Iterator[str]:
        """Yields code using configurations from instance variables. """
        yield f"{self.image.name}: \n  Skills: \n"
        for y_index, colors_at_y in enumerate(self.image.pixel_colors):
            for x_index, color_at_xy in enumerate(colors_at_y):
                if color_at_xy[3] == 0:
                    continue
                # pylint: disable-next=C0209,C0301
                yield "    - effect:particles{{particle={p};amount=1;color={c};Size={s};forwardOffset={fo};sideOffset={so};yOffset={y}}}\n".format(
                    p=self.particle_type.value,
                    c="#{0:02x}{1:02x}{2:02x}".format(  # pylint: disable=C0209
                        color_at_xy[0],
                        color_at_xy[1],
                        color_at_xy[2]
                    ),
                    # Number rounding is needed due to inaccuracy on floating point
                    # number calculations
                    s=round(color_at_xy[3] / 255 * self.particle_size, 3),
                    fo=round(self.foward_offset + y_index * self.particle_interval, 3) \
                    if self.mode is Mode.VERTICAL else round(self.foward_offset, 3),
                    so=round(self.side_offset - x_index * self.particle_interval, 3),
                    y=round(self.y_offset, 3) if self.mode is Mode.VERTICAL \
                    else round(self.y_offset - y_index * self.particle_interval, 3)
                )
