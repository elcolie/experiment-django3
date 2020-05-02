import json


def extract_params(input):
    dict_str = f"{ {input} }".replace("'", '').replace('sumInsured', '"sum_insured"').replace('premium', '"premium"')
    output = json.loads(dict_str)
    return output
