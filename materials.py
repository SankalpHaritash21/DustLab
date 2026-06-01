from settings import *

materials = {
    SAND: {
        "name": "Sand",
        "color": (245, 235, 216),
        "density": 2,
        "type": "powder",
        "thermal_conductivity": 0.08,
        "specific_heat": 0.8
    },

    WATER: {
        "name": "Water",
        "color": (0, 0, 255),
        "density": 1,
        "type": "liquid",
        "thermal_conductivity": 0.2,
        "specific_heat": 4.0
    },

    LAVA:{
        "name": "Lava",
        "color": (255, 69, 0),
        "density": 3,
        "type": "liquid",
        "thermal_conductivity": 0.3,
        "specific_heat": 1.5
    },

    OIL:{
        "name": "Oil",
        "color": (50, 40, 30),
        "density": 0.5,
        "type": "liquid",
        "thermal_conductivity": 0.12,
        "specific_heat": 2.0
    },

    STONE:{
        "name": "Stone",
        "color": (90, 90, 100),
        "density": 4,
        "type": "solid",
        "thermal_conductivity": 0.12,
        "specific_heat": 1.0
    },

    FIRE:{
        "name": "Fire",
        "color": (255, 140, 0),
        "density": -1,
        "type": "gas",
        "thermal_conductivity": 0.4,
        "specific_heat": 0.1
    },

    SMOKE:{
        "name": "Smoke",
        "color": (170, 170, 170),
        "density": -0.5,
        "type": "gas",
        "thermal_conductivity": 0.03,
        "specific_heat": 0.3
    },

    STEAM:{
        "name": "Steam",
        "color": (220, 220, 225),
        "density": -0.3,
        "type": "gas",
        "thermal_conductivity": 0.08,
        "specific_heat": 1.5
    }

}