import json


# Save the world state to a JSON file

def save_world(grid):

    with open("world_save.json", "w") as file:
        json.dump(grid, file)

    print("World saved successfully.")


# Load the world state from a JSON file

def load_world():

    try:

        with open("world_save.json", "r") as file:
            print("World loaded successfully.")
            return json.load(file)


    except FileNotFoundError:
        print("No saved world found.")
        return None
