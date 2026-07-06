
from settings import *
import random


def create_cell(material, temperature=20):

    cell= {
        "material": material,
        "temperature": temperature
    }

    # Wetness metadata
    if material in [SAND, STONE, ASH, MOSS]:
        cell["wetness"] = 0

    if material == SAND:
        cell["bank_damage"] = 0

    # Fire METADATA

    if material == FIRE:
        cell["fuel"] = 100

    if material == WATER:
        cell["sediment"] = 0
        cell["velocity"] = 0
        cell["river_bias"] = random.choice([-1, 1])

    return cell