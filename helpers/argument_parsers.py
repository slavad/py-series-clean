import helpers.input_validators as iv
def parse_common_series_args(parser):
    """these args are common for estimate_treshold and py_series_clean"""
    parser.add_argument(
        '-f',
        required = True,
        help='input file location, input file should be a text file of two columns: "time value"',
        metavar='INPUT'
    )
    parser.add_argument(
        '-o',
        required = True,
        help='output file location"',
        metavar='OUTPUT'
    )
    khi_default = 4
    khi_help = 'scale coefficient for the size of the dirty spectrum, see eq 147 in ref 2,'
    khi_help += ' default value is {}'.format(khi_default)
    parser.add_argument(
        '-k',
        required = False,
        help = khi_help,
        metavar ='KHI',
        default = khi_default,
        type = iv.check_positive_int
    )
