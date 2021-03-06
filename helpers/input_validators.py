import argparse

def check_inclusion_in_unity(value):
    """checks value that should be 0<x<=1"""
    number = check_positive_float(value)
    if number <= 0 or number > 1:
        raise argparse.ArgumentTypeError("value must be > 0 and <= 1, but your's is %s" % value)
    return number

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

def str2bool(v):
    true_vals = ('yes', 'true', 't', 'y', '1')
    false_vals = ('no', 'false', 'f', 'n', '0')
    if v.lower() in true_vals:
        return True
    elif v.lower() in false_vals:
        return False
    else:
        msg = '{} is not a boolean value,'.format(v)
        msg += ' allowed values (case insensitive) for True: {}'.format(', '.join(true_vals))
        msg += ' and for False: {}'.format(', '.join(false_vals))
        raise argparse.ArgumentTypeError(msg)