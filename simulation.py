import random

from settings import *
from materials import materials
from cell import create_cell
from systems.gas_system import update_gases
from systems.liquid_system import update_liquids
from systems.powder_system import update_powders
from simulation_utils import get_density, get_type, get_material
from systems.plant_system import update_plants
from systems.wetness_system import update_wetness

def update_simulation(grid):

    updated = set()

    
    # powder SIMULATION
    update_powders(grid, updated)
    
    # liquid SIMULATION
    update_liquids(grid, updated)

    # wetness SIMULATION
    update_wetness(grid)
    

    # gas SIMULATION
    update_gases(grid, updated)

    # plant SIMULATION
    update_plants(grid, updated)

    
    

   

                