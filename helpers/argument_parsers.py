import helpers.input_validators as iv
def parse_common_series_args(parser):
    """these args are common for estimate_noise_probability and clean"""
    parser.add_argument(
        '-i',
        required = True,
        help='input file location, input file should be a text file of two columns: "time value"',
        metavar='INPUT'
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


    use_aver_default = False
    use_aver_help = 'use average distance between points on the time grid'
    use_aver_help += ' default value is {}, if set to False then minimum distance is used'.format(khi_default)
    parser.add_argument(
        '-u',
        required = False,
        help = use_aver_help,
        metavar ='USE_AVERAGE',
        default = use_aver_default,
        type = iv.str2bool
    )
