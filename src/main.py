import json;
from termcolor import cprint

import user_reader

NUM_SELECTED_COLORS = 5
NUM_CORE_VALUES_FROM_INPUT = 6

COLORS = {
    "red": [255, 0, 0],
    "yellow": [255,255,0],
    "green": [0, 255, 0],
    "blue":  [0, 0, 255],
    "pink": [255,105,180],
    "orange": [255,165,0],
    "violete": [153,50,204],
    "brown": [139,69,19],
    "black": [0,0,0],
    "white": [245,245,245],
    "gray": [170,170,170]
}

color_qualities = json.load(open("../res/color_qualities.json"))
color_info = json.load(open("../res/color_info.json"))

def merge_user_qualities_to_core_values(user_qualities):
    core_values = user_qualities["core values"]

    # make core values a dictionary with weights
    new_core_values = {}
    for value in core_values:
        new_core_values[value] = 1

    # merge users input of core values with their personality traits and sources of pride
    merge_significance = 0 # must be a percentage
    personality_traits = user_qualities["personality traits"]
    merged_core_values = new_core_values # work in progress

    return merged_core_values

def find_color_weights(user_values):

    # find the weights of each color based on the core values
    weights_of_colors = {}
    for color_name in color_qualities:
        weight_of_color = 0

        # the core values that the current color has
        color_values = color_qualities[color_name]["core values"]

        # iterate over all of the color values
        for color_value_key, color_value in color_values.items():

            # iterate over user values
            for user_value_key, user_value in user_values.items():
                
                # check if the user value key is the color value key. If not, get the next user value key or end the loop
                if user_value_key != color_value_key:
                    continue

                # `user_value` is how much of the core value the user has. `color_value` is how much the color is affected by the core value
                # dividing the product by `NUM_CORE_VALUES_FROM_INPUT` keeps the weight as a percentage
                weight_of_color += color_value * user_value / float(NUM_CORE_VALUES_FROM_INPUT)

                break

        weights_of_colors[color_name] = weight_of_color

    return weights_of_colors

def pick_largest_weight(value_set):
    max_value = -1.0
    max_key = 0
    for (key, value) in value_set.items():
        if value > max_value:
            max_value = value
            max_key = key
    return max_key
    

def find_top_n_weight_keys(value_set, n):

    # prevent mutating the paramater
    value_set = value_set.copy()

    result = []
    for _count in range(0, n):
        max_key = pick_largest_weight(value_set)

        value_set.pop(max_key)
        result.append(max_key)

    return result


def print_color(color_name, text):
    color_rgb = COLORS[color_name]
    cprint("\033[38;2;" + str(color_rgb[0]) + ";" + str(color_rgb[1]) + ";" + str(color_rgb[2]) + "m" + text + "\033[0m")

# 1. record the user's traits & values
user_qualities = user_reader.get_user_qualities(NUM_CORE_VALUES_FROM_INPUT, 5)

# 2. compress all of user qualities into core values to make the next step simpler
user_values = merge_user_qualities_to_core_values(user_qualities)

# 2. give weights to the colors based on how relevant they are to the user's qualities
color_weights = find_color_weights(user_values)

# 3. pick the N most relavant colors
top_color_names = find_top_n_weight_keys(color_weights, NUM_SELECTED_COLORS)

# 5. display the colors

print("| these are your colors from most to least significant: \n")

for i in range(0, NUM_SELECTED_COLORS):
    color_name = top_color_names[i]
    color_weight = int(color_weights[color_name] * 100)

    print_color(color_name, "| - " + color_name + ": " + str(color_weight) + "% match")

color_names = list(color_info.keys())

while True:
    print("type a color to learn more about it. Type 'exit' to exit the program: ")
    response = input().lower()

    if response == "exit":
        break

    if response in color_names:
        print_color(response, response[0].upper() + response[1:] + ": ")
        for attribute in color_info[response]:
            print_color(response, f" - {attribute}")
        continue
    
    print(f"could not find '{response}'")