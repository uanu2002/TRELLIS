import random
import json

def random_subset(input_list, subset_size=None):
    if subset_size is None:
        subset_size = random.randint(1, len(input_list))

    if subset_size < 0 or subset_size > len(input_list):
        return "Invalid subset size"
    
    return random.sample(input_list, subset_size)

def json_to_user_prompt_T8(json_file):
    """Convert a JSON file to a user prompt string."""
    with open(json_file, 'r') as f:
        data = json.load(f)

    for geom in data['geometries']:
        if geom['type'] == 'Fuselage':
            Fuselage_Length = geom['parameters']['Length']
            Fuselage_Tess_U = geom['parameters']['Tess_U']
            Fuselage_Tess_W = geom['parameters']['Tess_W']
            Fuselage_Scale = geom['parameters']['Scale']
        elif geom['type'] == 'Wing':
            if geom['name'] == 'Wing':
                Wing_Span = geom['parameters']['Span']
                Wing_Sweep = geom['parameters']['Sweep']
                Wing_Twist = geom['parameters']['Twist']
                Wing_Root_Chord = geom['parameters']['Root_Chord']
                Wing_Tip_Chord = geom['parameters']['Tip_Chord']
                Wing_Tess_U = geom['parameters']['Tess_U']
                Wing_Tess_W = geom['parameters']['Tess_W']
                Wing_Scale = geom['parameters']['Scale']
            elif geom['name'] == 'HT':
                HT_Span = geom['parameters']['Span']
                HT_Sweep = geom['parameters']['Sweep']
                HT_Twist = geom['parameters']['Twist']
                HT_Root_Chord = geom['parameters']['Root_Chord']
                HT_Tip_Chord = geom['parameters']['Tip_Chord']
                HT_Tess_U = geom['parameters']['Tess_U']
                HT_Tess_W = geom['parameters']['Tess_W']
                HT_Scale = geom['parameters']['Scale']
            elif geom['name'] == 'VT':
                VT_Span = geom['parameters']['Span']
                VT_Sweep = geom['parameters']['Sweep']
                VT_Twist = geom['parameters']['Twist']
                VT_Root_Chord = geom['parameters']['Root_Chord']
                VT_Tip_Chord = geom['parameters']['Tip_Chord']
                VT_Tess_U = geom['parameters']['Tess_U']
                VT_Tess_W = geom['parameters']['Tess_W']
                VT_Scale = geom['parameters']['Scale']
    # Generate user prompt based on the extracted parameters
    user_prompt = "Generate a commercial aircraft with aerodynamic layout T8 the following specifications:\n"

    user_prompt_options = {
        "Fuselage": f"Fuselage: Length = {Fuselage_Length:.2f} m, Tessellation U = {Fuselage_Tess_U:.2f}, Tessellation W = {Fuselage_Tess_W:.2f}, Scale = {Fuselage_Scale:.2f}",
        "Main Wing": f"Main Wing: Span = {Wing_Span:.2f} m, Sweep = {Wing_Sweep:.2f} degrees, Twist = {Wing_Twist:.2f} degrees, Root Chord = {Wing_Root_Chord:.2f} m, Tip Chord = {Wing_Tip_Chord:.2f} m, Tessellation U = {Wing_Tess_U:.2f}, Tessellation W = {Wing_Tess_W:.2f}, Scale = {Wing_Scale:.2f}",
        "Horizontal Tail": f"Horizontal Tail: Span = {HT_Span:.2f} m, Sweep = {HT_Sweep:.2f} degrees, Twist = {HT_Twist:.2f} degrees, Root Chord = {HT_Root_Chord:.2f} m, Tip Chord = {HT_Tip_Chord:.2f} m, Tessellation U = {HT_Tess_U:.2f}, Tessellation W = {HT_Tess_W:.2f}, Scale = {HT_Scale:.2f}",
        "Vertical Tail": f"Vertical Tail: Span = {VT_Span:.2f} m, Sweep = {VT_Sweep:.2f} degrees, Twist = {VT_Twist:.2f} degrees, Root Chord = {VT_Root_Chord:.2f} m, Tip Chord = {VT_Tip_Chord:.2f} m, Tessellation U = {VT_Tess_U:.2f}, Tessellation W = {VT_Tess_W:.2f}, Scale = {VT_Scale:.2f}"
    }

    user_prompt_options_sets = {
        "Fuselage": [f"Length = {Fuselage_Length:.2f} m",
                     f"Tessellation U = {Fuselage_Tess_U:.2f}",
                     f"Tessellation W = {Fuselage_Tess_W:.2f}",
                     f"Scale = {Fuselage_Scale:.2f}"],
        "Main Wing": [f"Span = {Wing_Span:.2f} m",
                      f"Sweep = {Wing_Sweep:.2f} degrees",
                      f"Twist = {Wing_Twist:.2f} degrees",
                      f"Root Chord = {Wing_Root_Chord:.2f} m",
                      f"Tip Chord = {Wing_Tip_Chord:.2f} m",
                      f"Tessellation U = {Wing_Tess_U:.2f}",
                      f"Tessellation W = {Wing_Tess_W:.2f}",
                      f"Scale = {Wing_Scale:.2f}"],
        "Horizontal Tail": [f"Span = {HT_Span:.2f} m",
                            f"Sweep = {HT_Sweep:.2f} degrees",
                            f"Twist = {HT_Twist:.2f} degrees",
                            f"Root Chord = {HT_Root_Chord:.2f} m",
                            f"Tip Chord = {HT_Tip_Chord:.2f} m",
                            f"Tessellation U = {HT_Tess_U:.2f}",
                            f"Tessellation W = {HT_Tess_W:.2f}",
                            f"Scale = {HT_Scale:.2f}"],
        "Vertical Tail": [f"Span = {VT_Span:.2f} m",
                            f"Sweep = {VT_Sweep:.2f} degrees",
                            f"Twist = {VT_Twist:.2f} degrees",
                            f"Root Chord = {VT_Root_Chord:.2f} m",
                            f"Tip Chord = {VT_Tip_Chord:.2f} m",
                            f"Tessellation U = {VT_Tess_U:.2f}",
                            f"Tessellation W = {VT_Tess_W:.2f}",
                            f"Scale = {VT_Scale:.2f}"]
    }

    # Randomly select a subset of options for each component
    questions = user_prompt
    for component, options in user_prompt_options_sets.items():
        selected_options = random_subset(options, subset_size=random.randint(1, len(options)))
        questions += f"{component} specifications:\n"
        for option in selected_options:
            if random.choice([True, False]):
                questions += f"- {option}\n"
        questions += "\n"

    return questions

def json_to_user_prompt_f02(json_file):
    """Convert a JSON file to a user prompt string."""
    with open(json_file, 'r') as f:
        data = json.load(f)

    for geom in data['geometries']:
        if geom['type'] == 'Fuselage' and geom['name'] == 'Fuselage':
            Fuselage_Length = geom['parameters']['Length']
            Fuselage_Tess_U = geom['parameters']['Tess_U']
            Fuselage_Tess_W = geom['parameters']['Tess_W']
            Fuselage_X_Location = geom['parameters']['X_Location']
        elif geom['type'] == 'Wing' and geom['name'] == 'main wing':
            main_wing_Tess_U = geom['parameters']['Tess_U']
            main_wing_Tess_W = geom['parameters']['Tess_W']
            main_wing_X_Location = geom['parameters']['X_Location']
        elif geom['type'] == 'Wing' and geom['name'] == 'main wing_sec1':
            main_wing_sec1_Span = geom['parameters']['Span']
            main_wing_sec1_Chord = geom['parameters']['Chord']
            main_wing_sec1_Sweep = geom['parameters']['Sweep']
            main_wing_sec1_Twist = geom['parameters']['Twist']
            main_wing_sec1_Root_Chord = geom['parameters']['Root_Chord']
            main_wing_sec1_Tip_Chord = geom['parameters']['Tip_Chord']
        elif geom['type'] == 'Wing' and geom['name'] == 'main wing_sec2':
            main_wing_sec2_Span = geom['parameters']['Span']
            main_wing_sec2_Chord = geom['parameters']['Chord']
            main_wing_sec2_Sweep = geom['parameters']['Sweep']
            main_wing_sec2_Twist = geom['parameters']['Twist']
            main_wing_sec2_Root_Chord = geom['parameters']['Root_Chord']
            main_wing_sec2_Tip_Chord = geom['parameters']['Tip_Chord']
        elif geom['type'] == 'Wing' and geom['name'] == 'horizontal stabilizer':
            horizontal_stabilizer_Tess_U = geom['parameters']['Tess_U']
            horizontal_stabilizer_Tess_W = geom['parameters']['Tess_W']
            horizontal_stabilizer_X_Location = geom['parameters']['X_Location']
            horizontal_stabilizer_Y_Location = geom['parameters']['Y_Location']
            horizontal_stabilizer_Z_Location = geom['parameters']['Z_Location']
        elif geom['type'] == 'Wing' and geom['name'] == 'horizontal stabilizer_sec1':
            horizontal_stabilizer_sec1_Span = geom['parameters']['Span']
            horizontal_stabilizer_sec1_Chord = geom['parameters']['Chord']
            horizontal_stabilizer_sec1_Sweep = geom['parameters']['Sweep']
            horizontal_stabilizer_sec1_Twist = geom['parameters']['Twist']
            horizontal_stabilizer_sec1_Root_Chord = geom['parameters']['Root_Chord']
            horizontal_stabilizer_sec1_Tip_Chord = geom['parameters']['Tip_Chord']
        elif geom['type'] == 'Wing' and geom['name'] == 'vertical stabilizer':
            vertical_stabilizer_Tess_U = geom['parameters']['Tess_U']
            vertical_stabilizer_Tess_W = geom['parameters']['Tess_W']
            vertical_stabilizer_X_Location = geom['parameters']['X_Location']
            vertical_stabilizer_Y_Location = geom['parameters']['Y_Location']
            vertical_stabilizer_Z_Location = geom['parameters']['Z_Location']
        elif geom['type'] == 'Wing' and geom['name'] == 'vertical stabilizer_sec1':
            vertical_stabilizer_sec1_Span = geom['parameters']['Span']
            vertical_stabilizer_sec1_Chord = geom['parameters']['Chord']
            vertical_stabilizer_sec1_Sweep = geom['parameters']['Sweep']
            vertical_stabilizer_sec1_Twist = geom['parameters']['Twist']
            vertical_stabilizer_sec1_Root_Chord = geom['parameters']['Root_Chord']
            vertical_stabilizer_sec1_Tip_Chord = geom['parameters']['Tip_Chord']
    # Generate user prompt based on the extracted parameters
    user_prompt = "Generate a commercial aircraft with aerodynamic layout f02 the following specifications:\n"


    user_prompt_options = {
        "Fuselage": f"Fuselage: Length = {Fuselage_Length:.2f} m, Tessellation U = {Fuselage_Tess_U:.2f}, Tessellation W = {Fuselage_Tess_W:.2f}, X Location = {Fuselage_X_Location:.2f}",
        "Main Wing": f"Main Wing: Tessellation U = {main_wing_Tess_U:.2f}, Tessellation W = {main_wing_Tess_W:.2f}, X Location = {main_wing_X_Location:.2f}",
        "Main Wing Section 1": f"Main Wing Section 1: Span = {main_wing_sec1_Span:.2f} m, Chord = {main_wing_sec1_Chord:.2f} m, Sweep = {main_wing_sec1_Sweep:.2f} degrees, Twist = {main_wing_sec1_Twist:.2f} degrees, Root Chord = {main_wing_sec1_Root_Chord:.2f} m, Tip Chord = {main_wing_sec1_Tip_Chord:.2f} m",
        "Main Wing Section 2": f"Main Wing Section 2: Span = {main_wing_sec2_Span:.2f} m, Chord = {main_wing_sec2_Chord:.2f} m, Sweep = {main_wing_sec2_Sweep:.2f} degrees, Twist = {main_wing_sec2_Twist:.2f} degrees, Root Chord = {main_wing_sec2_Root_Chord:.2f} m, Tip Chord = {main_wing_sec2_Tip_Chord:.2f} m",
        "Horizontal Stabilizer": f"Horizontal Stabilizer: Tessellation U = {horizontal_stabilizer_Tess_U:.2f}, Tessellation W = {horizontal_stabilizer_Tess_W:.2f}, X Location = {horizontal_stabilizer_X_Location:.2f}, Y Location = {horizontal_stabilizer_Y_Location:.2f}, Z Location = {horizontal_stabilizer_Z_Location:.2f}",
        "Horizontal Stabilizer Section 1": f"Horizontal Stabilizer Section 1: Span = {horizontal_stabilizer_sec1_Span:.2f} m, Chord = {horizontal_stabilizer_sec1_Chord:.2f} m, Sweep = {horizontal_stabilizer_sec1_Sweep:.2f} degrees, Twist = {horizontal_stabilizer_sec1_Twist:.2f} degrees, Root Chord = {horizontal_stabilizer_sec1_Root_Chord:.2f} m, Tip Chord = {horizontal_stabilizer_sec1_Tip_Chord:.2f} m",
        "Vertical Stabilizer": f"Vertical Stabilizer: Tessellation U = {vertical_stabilizer_Tess_U:.2f}, Tessellation W = {vertical_stabilizer_Tess_W:.2f}, X Location = {vertical_stabilizer_X_Location:.2f}, Y Location = {vertical_stabilizer_Y_Location:.2f}, Z Location = {vertical_stabilizer_Z_Location:.2f}",
        "Vertical Stabilizer Section 1": f"Vertical Stabilizer Section 1: Span = {vertical_stabilizer_sec1_Span:.2f} m, Chord = {vertical_stabilizer_sec1_Chord:.2f} m, Sweep = {vertical_stabilizer_sec1_Sweep:.2f} degrees, Twist = {vertical_stabilizer_sec1_Twist:.2f} degrees, Root Chord = {vertical_stabilizer_sec1_Root_Chord:.2f} m, Tip Chord = {vertical_stabilizer_sec1_Tip_Chord:.2f} m"
    }

    user_prompt_options_sets = {
        "Fuselage": [f"Length = {Fuselage_Length:.2f} m",
                     f"Tessellation U = {Fuselage_Tess_U:.2f}",
                     f"Tessellation W = {Fuselage_Tess_W:.2f}",
                     f"X Location = {Fuselage_X_Location:.2f}"],
        "Main Wing": [f"Tessellation U = {main_wing_Tess_U:.2f}",
                      f"Tessellation W = {main_wing_Tess_W:.2f}",
                      f"X Location = {main_wing_X_Location:.2f}"],
        "Main Wing Section 1": [f"Span = {main_wing_sec1_Span:.2f} m",
                                f"Chord = {main_wing_sec1_Chord:.2f} m",
                                f"Sweep = {main_wing_sec1_Sweep:.2f} degrees",
                                f"Twist = {main_wing_sec1_Twist:.2f} degrees",
                                f"Root Chord = {main_wing_sec1_Root_Chord:.2f} m",
                                f"Tip Chord = {main_wing_sec1_Tip_Chord:.2f} m"],
        "Main Wing Section 2": [f"Span = {main_wing_sec2_Span:.2f} m",
                                f"Chord = {main_wing_sec2_Chord:.2f} m",
                                f"Sweep = {main_wing_sec2_Sweep:.2f} degrees",
                                f"Twist = {main_wing_sec2_Twist:.2f} degrees",
                                f"Root Chord = {main_wing_sec2_Root_Chord:.2f} m",
                                f"Tip Chord = {main_wing_sec2_Tip_Chord:.2f} m"],
        "Horizontal Stabilizer": [f"Tessellation U = {horizontal_stabilizer_Tess_U:.2f}",
                                   f"Tessellation W = {horizontal_stabilizer_Tess_W:.2f}",
                                   f"X Location = {horizontal_stabilizer_X_Location:.2f}",
                                   f"Y Location = {horizontal_stabilizer_Y_Location:.2f}",
                                   f"Z Location = {horizontal_stabilizer_Z_Location:.2f}"],
        "Horizontal Stabilizer Section 1": [f"Span = {horizontal_stabilizer_sec1_Span:.2f} m",
                                       f"Chord = {horizontal_stabilizer_sec1_Chord:.2f} m",
                                       f"Sweep = {horizontal_stabilizer_sec1_Sweep:.2f} degrees",
                                       f"Twist = {horizontal_stabilizer_sec1_Twist:.2f} degrees",
                                       f"Root Chord = {horizontal_stabilizer_sec1_Root_Chord:.2f} m",
                                       f"Tip Chord = {horizontal_stabilizer_sec1_Tip_Chord:.2f} m"],
        "Vertical Stabilizer": [f"Tessellation U = {vertical_stabilizer_Tess_U:.2f}",
                                f"Tessellation W = {vertical_stabilizer_Tess_W:.2f}",
                                f"X Location = {vertical_stabilizer_X_Location:.2f}",
                                f"Y Location = {vertical_stabilizer_Y_Location:.2f}",
                                f"Z Location = {vertical_stabilizer_Z_Location:.2f}"],
        "Vertical Stabilizer Section 1": [f"Span = {vertical_stabilizer_sec1_Span:.2f} m",
                                          f"Chord = {vertical_stabilizer_sec1_Chord:.2f} m",
                                          f"Sweep = {vertical_stabilizer_sec1_Sweep:.2f} degrees",
                                          f"Twist = {vertical_stabilizer_sec1_Twist:.2f} degrees",
                                          f"Root Chord = {vertical_stabilizer_sec1_Root_Chord:.2f} m",
                                          f"Tip Chord = {vertical_stabilizer_sec1_Tip_Chord:.2f} m"]
    }


    # Randomly select a subset of options for each component
    questions = user_prompt
    for component, options in user_prompt_options_sets.items():
        selected_options = random_subset(options, subset_size=random.randint(1, len(options)))
        
        questions_for_component = ""
        attribution_activated = False
        questions_for_component += f"{component} specifications:\n"
        for option in selected_options:
            if random.choice([True, False]):
                questions_for_component += f"- {option}\n"
                attribution_activated = True
            else:
                pass
        if attribution_activated:
            questions += questions_for_component
            questions += "\n"

    return questions

def json2prompt(json_file):
    json_path = str(json_file)
    if 'f02' in json_path:
        func = json_to_user_prompt_f02
    elif 'T8' in json_path:
        func = json_to_user_prompt_T8
    return func(json_file)



if __name__ == "__main__":
    import os
    import pathlib

    # Define the directory containing the JSON files
    json_dir = "/mnt/d/Dataset/airfoil3D/T8/json"
    json_dir = pathlib.Path(json_dir)

    # Iterate through all JSON files in the directory
    for json_file in os.listdir(json_dir):
        if json_file.endswith(".json") and json_file.startswith("T8_sample_"):
            full_path = os.path.join(json_dir, json_file)
            user_prompt = json_to_user_prompt(full_path)
            print(f"User prompt for {json_file}:\n{user_prompt}\n")
