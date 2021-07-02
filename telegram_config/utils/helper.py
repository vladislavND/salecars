

def without_keys(d: dict, keys) -> dict:
    return {x: d[x] for x in d if x not in keys}