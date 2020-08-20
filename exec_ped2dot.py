#!/usr/bin/python3
"""
Ped2Dot is a python program allowing to automaticaly produce a genealogical tree and the
associated dot file from a pedigree file.

Usage:
    exec_ped2dot.py <input_file>

Options:
    -h, --help                      Show this screen.
    -v, --version                   Show version.
"""
##########
# IMPORT #
##########
from docopt import docopt
from ped2dot.ped2dot import ped_to_dot

########
# MAIN #
########
def main(argument):
    ped_to_dot(argument["<input_file>"])

########
# EXEC #
########
if __name__ == '__main__':
    arguments = docopt(__doc__, version = "1.0")
    main(arguments)
