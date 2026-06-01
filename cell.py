
from settings import *


def create_cell(material, temperature=20):

    cell= {
        "material": material,
        "temperature": temperature
    }

    # Fire METADATA

    if material == FIRE:
        cell["fuel"] = 100

    return cell