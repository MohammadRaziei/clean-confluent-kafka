from __future__ import annotations

import yaml

import fastnumbers


def convert_string_to_yaml_number(string):
    return yaml.safe_load(string)


def convert_string_to_real_number(string):
    return fastnumbers.try_real(string, on_fail=fastnumbers.INPUT)


def replace_self_with_value(d):
    if isinstance(d, dict):
        if len(d) == 1 and 'self' in d:
            return d['self']
        else:
            for key, value in d.items():
                d[key] = replace_self_with_value(value)
    return d


def reverse_flatten_dict(flattened_dict, sep="."):
    hierarchical_dict = {}
    for key, value in flattened_dict.items():
        keys = key.split(sep)
        current_dict = hierarchical_dict
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = {}
            current_dict = current_dict[k]
        current_key = keys[-1]
        current_dict[current_key] = {'self': value}
    return replace_self_with_value(hierarchical_dict)


def unflatten_dict(d, sep="."):
    result = dict()
    for key, value in d.items():
        parts = key.split(sep)
        part = parts[0]
        if part not in result:
            result[part] = dict()
        if len(parts) > 1:
            result[part][sep.join(parts[1:])] = value
    return result


def flatten_dict(hierarchical_dict, parent_key="", sep="."):
    items = []
    for key, value in hierarchical_dict.items():
        new_key = (f"{parent_key}{sep}{key}" if parent_key else key) \
            if key != "self" else parent_key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, sep).items())
        else:
            items.append((new_key, value))
    return dict(items)

