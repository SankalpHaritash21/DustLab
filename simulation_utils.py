from settings import *
from materials import materials


def get_density(material_id):
    if material_id == 0:
        return -1
    
    return materials[material_id]["density"]

def get_type(material_id):
    if material_id == 0:
        return None
    
    return materials[material_id]["type"]

def get_material(cell):

    if cell == 0:
        return 0

    return cell["material"]