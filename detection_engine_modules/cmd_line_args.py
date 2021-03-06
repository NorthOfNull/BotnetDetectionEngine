"""
The cmd_line_args Module.
"""

import argparse

def get_cmd_line_args():
    """
    Parses the command line arguments.

    Returns:
        args (dict): A populated dictionary, containing the parsed arguments from sys.argv.
    """
    parser = argparse.ArgumentParser(description=
                                     """The Botnet Detection Engine.
                                     GUI and logging is enabled by default.""")

    # Add arguments
    parser.add_argument("-g", "--no-gui", action="store_false",
                        help="Disables GUI.", default=True)

    parser.add_argument("-l", "--no-log", action="store_false",
                        help="Disables alert and flow logging to file.", default=True)

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable verbose debugging output.", default=False)

    parser.add_argument("-r", "--read", action="store",
                        help="Read from \'.pcap\' or Network Flow file.", default=False)

    # Parse arguments
    args = parser.parse_args()
    args = vars(args)

    return args
