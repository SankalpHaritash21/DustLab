import random

from settings import *
from materials import materials
from cell import create_cell
from systems.gas_system import update_gases
from systems.liquid_system import update_liquids
from systems.powder_system import update_powders
from simulation_utils import get_density, get_type, get_material

def update_simulation(grid):

    updated = set()

    
    # powder SIMULATION
    update_powders(grid, updated)
    
    # liquid SIMULATION
    update_liquids(grid, updated)
    

    # gas SIMULATION
    update_gases(grid, updated)
    

   

                