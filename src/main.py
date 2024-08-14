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

        # the names of core values that the user has
        user_value_keys = list(user_values.keys())

        # iterate over all of the color values
        for color_value_key, color_value in color_values.items():

            # iterate over user values
            for user_value_key, user_value in user_values.items():
                
                # check if the user value key is the color value key. If not, get the next user value key or end the loop
                if user_value_key != color_value_key:
                    continue

                # `user_value` is how much of the core value the user has. `color_value` is how much the color is affected by the core value
                weight_of_color += color_value * user_value

                break

        weights_of_colors[color_name] = weight_of_color

    return weights_of_colors


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

# 2. compress all of user qualities into core values to make the next step simpler
user_values = merge_user_qualities_to_core_values(user_qualities)

# 2. give weights to the colors based on how relevant they are to the user's qualities
color_weights = find_color_weights(user_values)

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
