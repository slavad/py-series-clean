import helpers.input_validators as iv
def parse_common_series_args(parser):
    """these args are common for estimate_detection_treshold and clean"""
    parser.add_argument(
        '-i',
        required = True,
        help='input file location, input file should be a text file of two columns: "time value"',
        metavar='INPUT'
    )
