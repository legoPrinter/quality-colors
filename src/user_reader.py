import json

common_qualities = json.load(open("../res/common_qualities.json"))

example_user_qualities = {
    "core values": ["humility", "gratitude", "perseverance", "optimism", "curiosity", "creativity"],
    "sources of pride": ["painting", "running", "puzzles", "card collecting", "career"],
    "personality traits": {
        "openness": 1,
        "conscientiousness": 5,
        "extraversion": 2,
        "agreeableness": 4,
        "neuroticism": 2
    }
}

def print_list_ordered(items):
    items_length = len(items)
    index = 0

    while index < items_length:
        item = items[index]
        index += 1
        print(f"{index}. {item}")

def get_user_choises(items, amount_choises, key_word):
    items_length = len(items)

    if items_length < amount_choises:
        raise Exception("Number of choises exceeds list length")

    choises_left = amount_choises

    choises = []

    while choises_left != 0:
        print_list_ordered(items)
        if choises_left == amount_choises:
            print(f"choose {amount_choises} {key_word} from the list: ")
        else:
            choise_or_choises = "choises"
            if choises_left == 1: 
                "choise"

            print(f"you have {choises_left} {choise_or_choises} left: ")

        # get user input
        choise = input()

        # try to parse the user input
        try:
            choise = int(choise)
        except ValueError:
            print("please enter a number")
            continue

        # check if the input is in bounds
        if choise < 1 or choise > items_length:
            print("please choose a number from one of the lables")
            continue

        # at this point, the choise is validated. Decrement the choises left
        choises_left -= 1

        # print the user's choise
        print(f"your choise was: #{choise}. {items[choise-1]}")

        # remove the user's choise from the list
        item_chosen = items[choise-1]
        del items[choise-1]
        items_length -= 1

        # add the user's choise to the list of choises
        choises.append(item_chosen)

    return choises

def get_user_choises_from_categories(categories, amount_choises, key_word):
    choises_left = amount_choises

    choises = []

    print(f"choose {amount_choises} {key_word} from the list.")

    while choises_left != 0:
        # print the category names
        category_names = list(categories.keys())
        print_list_ordered(category_names)

        # get the users category
        print("pick a category to view it: ")
        choise = input()

        # try to parse the user input
        try:
            choise = int(choise)
        except ValueError:
            print("please enter a number")
            continue

        # check if the input is in bounds
        if choise < 1 or choise > len(category_names):
            print("please choose a number from one of the lables")
            continue

        chosen_category_name = category_names[choise-1]
        category_items = categories[chosen_category_name]
        category_items_length = len(category_items)

        while True:

            # display the list in the category
            print(f"{chosen_category_name}:")
            print_list_ordered(category_items)

            # print how mutch choises the user has
            choise_or_choises = "choises"
            if choises_left == 1: 
                "choise"
            print(f"you have {choises_left} {choise_or_choises} left.")

            # get user input
            print("Enter the number beside your choise, or type \"b\" to go back: ")
            choise = input()

            # check if the user wants to go back
            if choise == "b":
                break

            # try to parse the user input
            try:
                choise = int(choise)
            except ValueError:
                print("please enter a number")
                continue

            # check if the input is in bounds
            if choise < 1 or choise > category_items_length:
                print("please choose a number from one of the lables")

            # at this point, the choise is validated. Decrement the choises left
            choises_left -= 1

            # print the user's choise
            print(f"your choise was: #{choise}. {category_items[choise-1]}")

            # remove the user's choise from the list
            del categories[chosen_category_name][choise-1]

            # add the user's choise to the list of choises
            choises.append(choise-1)

            break

    return choises

def get_user_core_values(amount_choises):
    return get_user_choises(common_qualities["core values"], amount_choises, "of your core values")

def get_user_sources_of_pride(amount_choises):
    return get_user_choises_from_categories(common_qualities["sources of pride"], amount_choises, "of your sources of pride")

def get_user_personality_traits():
    personality_traits = common_qualities["personality traits"]

    user_personality_traits = {}

    index = 0

    print("now, rate how much you have these personality traits from 1 - 5 inclusively: ")
    while index < len(personality_traits):

        # print the trait
        personality_trait = personality_traits[index]
        print(f"{index + 1}. {personality_trait}: ")

        # get user input
        choise = input()

        # try to parse the user input
        try:
            choise = int(choise)
        except ValueError:
            print("please enter a number")
            continue

        # check if the input is in bounds
        if choise < 1 or choise > 5:
            print("please choose a number from one of the lables")
            continue

        # increment count
        index += 1
        
        # add the choise to the result
        user_personality_traits[personality_trait] = choise/5

    return user_personality_traits

def get_user_qualities(num_core_values, num_sources_of_pride):
    #return example_user_qualities # for debugging purposes

    # work in progress
    user_qualities = {
        "core values": get_user_core_values(num_core_values),
        "sources of pride": example_user_qualities["sources of pride"], #get_user_sources_of_pride(num_sources_of_pride),
        "personality traits": example_user_qualities["personality traits"] #get_user_personality_traits()
    }
    
    return user_qualities