from main_paths import get_large_traffic
import pandas as pd

def find_idea_window(effect_col, head_val, args, ds_path = get_large_traffic()):
    data = pd.read_csv(ds_path).head(head_val)
    unique_keys = data[effect_col].unique().tolist()

    effect_dict = {}
    cause_dict = {}

    for key in unique_keys:
        effect_dict[key] = {}

    for i in range(len(data[effect_col])):
        effect = data[effect_col][i]

        for cause_col in args:
            cause = data[cause_col][i]

            if not cause in effect_dict[effect]:
                effect_dict[effect][cause] = []

            for key in cause_dict.keys():
                if effect in cause_dict[key] and not cause_dict[key][effect] == None:
                    if key not in effect_dict[effect]:
                        effect_dict[effect][key] = []

                    new_val = i - cause_dict[key][effect]
                    effect_dict[effect][key].append(new_val)
                    cause_dict[key][effect] = None

        for cause_col in args:
            cause = data[cause_col][i]

            if not cause in cause_dict:
                cause_dict[cause] = {}

            for key in effect_dict.keys():
                cause_dict[cause][key] = i

    # for key in effect_dict.keys():
    #     print(f"{key}:")
    #     for key_2 in effect_dict[key]:
    #         print(f"  - {key_2} - {effect_dict[key][key_2]}")
    # print('\n\n\n')

    return effect_dict
