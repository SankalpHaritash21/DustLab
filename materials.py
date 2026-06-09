from settings import *

materials = {
    SAND: {
        "name": "Sand",
        "color": (245, 235, 216),
        "density": 2,
        "type": "powder",
        "thermal_conductivity": 0.08,
        "specific_heat": 0.8,
        "reactions":[
            { "with": FIRE, "min_temp": 700, "result_self": GLASS, "result_other": SAND }
        ]
    },

    WATER: {
        "name": "Water",
        "color": (0, 0, 255),
        "density": 1,
        "type": "liquid",
        "thermal_conductivity": 0.2,
        "specific_heat": 4.0,
        "boiling_point": 120,
        "boils_into": STEAM,
        
    },

    LAVA:{
        "name": "Lava",
        "color": (255, 69, 0),
        "density": 3,
        "type": "liquid",
        "thermal_conductivity": 0.25,
        "specific_heat": 8,
        "solidify_point": 400,
        "solidifies_into": STONE,
    },

    OIL:{
        "name": "Oil",
        "color": (50, 40, 30),
        "density": 0.5,
        "type": "liquid",
        "thermal_conductivity": 0.12,
        "specific_heat": 2.0,
        "ignition_point": 100,
        "ignites_into": FIRE,
        "fuel_value": 200,
   },

    STONE:{
        "name": "Stone",
        "color": (90, 90, 100),
        "density": 4,
        "type": "solid",
        "thermal_conductivity": 0.12,
        "specific_heat": 0.3,
        "melting_point": 600,

    },

    FIRE:{
        "name": "Fire",
        "color": (255, 140, 0),
        "density": -1,
        "type": "gas",
        "thermal_conductivity": 0.4,
        "specific_heat": 0.1,
        "heat_output": 4,
        "buoyancy": 1.0
    },

    SMOKE:{
        "name": "Smoke",
        "color": (170, 170, 170),
        "density": -0.5,
        "type": "gas",
        "thermal_conductivity": 0.03,
        "specific_heat": 0.3,
        "buoyancy": 0.6
    },

    STEAM:{
        "name": "Steam",
        "color": (220, 220, 225),
        "density": -0.3,
        "type": "gas",
        "thermal_conductivity": 0.08,
        "specific_heat": 1.5,
        "condensation_point": 25,
        "condenses_into": WATER,
        "buoyancy": 0.8
    },

    CRACKED_STONE: {
        "name": "Cracked Stone",
        "color": (60, 60, 60),
        "density": 4,
        "type": "solid",
        "thermal_conductivity": 0.12,
        "specific_heat": 1.0
    },

    GLASS: {
        "name": "Glass",
        "color": (100, 240, 255),
        "density": 4,
        "type": "solid",
        "thermal_conductivity": 0.05,
        "specific_heat": 0.2,
    },

    PLANT: {
        "name": "Plant",
        "color": (50, 180, 50),
        "density": 1,
        "type": "solid",
        "thermal_conductivity": 0.05,
        "specific_heat": 0.3,
        "ignition_point": 80,
        "ignites_into": FIRE,
    },
    ASH:{
        "name": "Ash",
        "color": (90, 90, 90),
        "density": 2,
        "type": "powder",
        "thermal_conductivity": 0.1,
        "specific_heat": 0.2,
    },
    SPRING: {
    "name": "Spring",
    "color": (80, 170, 255),
    "density": 5,
    "type": "solid",
    "thermal_conductivity": 0.1,
    "specific_heat": 1.0,
},

}