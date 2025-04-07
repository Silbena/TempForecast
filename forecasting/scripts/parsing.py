import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('save',
                        nargs='?',
                        type = int,
                        choices = [0,1],
                        default = 0,
                        help = '0 - show, 1 - save')
    args = parser.parse_args()

    return args