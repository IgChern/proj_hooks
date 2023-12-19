from typing import Union


def get_dict_path_or_none(element: dict, *keys: Union[str, int]) -> any:
    if not isinstance(element, dict) or len(keys) == 0:
        return None

    key_element = element
    for key in keys:
        try:
            key_element = key_element[key]
        except (KeyError, IndexError, TypeError):
            return None
    return key_element
