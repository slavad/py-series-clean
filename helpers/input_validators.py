import argparse

def check_positive_int(value):
    """parse and validate int argument value"""
    return check_positive(value, int)

def check_positive_float(value):
    """parse and validate float argument value"""
    return check_positive(value, float)

def check_positive(value, parser):
    """parse and validate argument value"""
    parsed_value = parser(value)
    if parsed_value < 0:
         raise argparse.ArgumentTypeError("%s is not a non-negative number" % value)
    return parsed_value