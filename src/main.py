import json;
from termcolor import cprint

import user_reader

NUM_SELECTED_COLORS = 5

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

def find_color_weights(user_qualities):

    inputed_core_values = user_qualities["core values"]

    # make core values a dictionary with weights
    core_values = {}
    for value in inputed_core_values:
        core_values[value] = 1

    # merge users input of core values with their personality traits and sources of pride
    new_core_values = core_values # work in progress

    # find the weights of each color based on the core values
    color_weights = {}
    for color_name in color_qualities:
        color_weight = 0

        qualities_of_color = color_qualities[color_name]
        color_core_values = qualities_of_color["core values"]
        color_core_value_names = color_core_values.keys()

        core_value_names = new_core_values.keys()

        for core_value_name in core_value_names:
            if not color_core_value_names.__contains__(core_value_name): continue
            color_weight += color_core_values[core_value_name] * new_core_values[core_value_name]

        color_weights[color_name] = color_weight

    return color_weights


def find_top_n_weight_keys(value_set, n):
    result = []
    for _count in range(0, n):
        max_value = -1
        max_key = 0
        for key in value_set:
            value = value_set[key]
            if value > max_value:
                max_value = value
                max_key = key
        result.append(max_key)
        value_set.pop(max_key)
    return result


# 1. record the user's traits & values
user_qualities = user_reader.get_user_qualities(5, 5)

# 2. give weights to the colors based on how relevant they are to the user's qualities
color_weights = find_color_weights(user_qualities)

# 3. pick the N most relavant colors
top_color_names = find_top_n_weight_keys(color_weights, NUM_SELECTED_COLORS)

# 4. convert the color names to rgb values
top_colors_rgb = []
for color_name in top_color_names:
    top_colors_rgb.append(COLORS[color_name])

# 5. display the colors

print("| these are your colors from most to least significant: \n")

for i in range(0, NUM_SELECTED_COLORS):
    color = top_colors_rgb[i]
    cprint("\033[38;2;" + str(color[0]) + ";" + str(color[1]) + ";" + str(color[2]) + "m| - " + top_color_names[i] + "\033[0m")
