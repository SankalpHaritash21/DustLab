
from settings import *


def create_cell(material, temperature=20):

    cell= {
        "material": material,
        "temperature": temperature
    }

    # Wetness metadata
    if material in [SAND, STONE, ASH, MOSS]:
        cell["wetness"] = 0

    # Fire METADATA

    if material == FIRE:
        cell["fuel"] = 100

    return cell