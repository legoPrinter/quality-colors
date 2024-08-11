import json;
from termcolor import cprint

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

trait_names = [
    "passionate", "formal", "creative", "optimistic", 
    "disciplined", "energetic", "happy", "elderly", "healthy",
    "wealthy", "authoritative"
]

pride_names = [
    "family", "religion", "friendship",
    "sports", "teaching", "shopping", 
    "education", "gaming", "exeresize", 
    "traveling", "work", "a simple lifestyle",
]

quality_names = trait_names + pride_names
qualities_length = len(quality_names)

color_qualities = json.load(open("color_qualities.json"))

def parse_user_input(value): 
    new_value = 0
    try:
        new_value = int(value)
    except ValueError:
        print(" (!) input must be a number")
        return None
    if new_value < 1 or new_value > 5:
        print(" (!) value must be between 1 and 5")
        return None
    return new_value

def get_user_qualities():
    user_qualities = {}

    print("enter your traits from 1 through 5:")
    for trait_name in trait_names:
        while True:
            value = parse_user_input(input("  -  how " + trait_name + " are you: "))
            if value == None: continue
            user_qualities[trait_name] = value
            break

    print("enter how much you value the following from 1 through 5:")
    for pride_name in pride_names:
        while True:
            value = parse_user_input(input("  -  do you value " + pride_name + ": "))
            if value == None: continue
            user_qualities[pride_name] = value
            break
    
    return user_qualities

def find_color_weights(user_qualities):
    # Color_qualities and it's children are dictionaries
    # Iterating over dictionaries provides their keys

    color_weights = {}

    for color_name in color_qualities:
        differences = 0
        color = color_qualities[color_name]
        for quality in color:
            difference = abs(color[quality] - user_qualities[quality])
            differences += difference

        # find the weight of the color. The smaller the difference, the bigger the weight
        color_weight = 1 - ((float(differences) / float(qualities_length)) / 4.0)

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
user_qualities = get_user_qualities()

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
