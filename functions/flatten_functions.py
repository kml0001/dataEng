from functions import export_functions


def flatten(dict_origin, dict_flattened):
    for key, value in dict_origin.items():
        if isinstance(value, dict):
            for k, v in value.items():
                dict_flattened[f'{key}_{k}'] = v
        elif isinstance(value, list):
            for var_dict in value:
                for var_k, var_v in var_dict.items():
                    dict_flattened[f'{key}_{var_k}'] = var_v
        else:
            dict_flattened[key] = value


def equalize_dictionaries(list_of_dicts):
    # Find all unique keys in the dictionaries
    all_keys = set()
    for dictionary in list_of_dicts:
        all_keys.update(dictionary.keys())

    # Iterate through each dictionary and add missing keys with a value of -1
    for dictionary in list_of_dicts:
        for key in all_keys:
            if key not in dictionary:
                dictionary[key] = -1


def flatten_data(data, path):
    flattened_data = []
    for d in data:
        flattened_d = {}
        flatten(d, flattened_d)
        flattened_data.append(flattened_d)

    equalize_dictionaries(flattened_data)
    export_functions.to_json(flattened_data, f'{path}.json')
    export_functions.to_csv(flattened_data,f'{path}.csv')
