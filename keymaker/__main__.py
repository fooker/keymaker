# import requests
# import bs4
# import urllib.parse

import sys

from keymaker import parser

from keymaker.store import Store
from keymaker.authority import Authority


parser.add_argument('-b', '--base',
                    dest='base_path',
                    type=str,
                    required=True,
                    metavar='PATH',
                    help='The path where all certificates are stored')

import keymaker.commands

if __name__ == '__main__':
    args = parser.parse_args()

    store = Store(base_path=args.base_path)

    try:
        args.func(store=store,
                  args=args)

    except Exception as e:
        raise
        # print(str(e), file=sys.stderr)
        #
        # sys.exit(1)
