def reverse_flatten_dict(d, sep="."):
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        d[parts[-1]] = value
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
