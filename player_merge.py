import argparse


def get_command_line_args():
    """Set up the CLI arguments and return the values"""

    parser = argparse.ArgumentParser(
        description='Merge multiple player databases together')

    parser.add_argument('files', metavar='files', nargs='+',
                        help='a list of player databases to merge')
    parser.add_argument('-o', dest='outfile', default='outfile.csv',
                        help='the destination file for the merged database')

    return parser.parse_args()


def get_input_files(*args):
    """Return a list of the inputted file names with their weights"""

    # check if arg list is even and every other arg is an integer
    if len(args) % 2 == 0 and all(x.isdigit() for x in args[1::2]):

        # return the args, all tupled up
        return zip(args[::2], args[1::2])

    else:

        # return each arg with a weight of 1
        return [(x, 1) for x in args]

if __name__ == '__main__':
    cli_args = get_command_line_args()

    input_files = get_input_files(*cli_args.files)
