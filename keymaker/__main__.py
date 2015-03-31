import sys

from keymaker import parser
from keymaker.store import Store


parser.add_argument('-b', '--base',
                    dest='base_path',
                    type=str,
                    required=True,
                    metavar='PATH',
                    help='The path where all certificates are stored')


from keymaker.commands import *


def main():
    # Parse the command line arguments
    args = parser.parse_args()

    try:
        # Create a store instance
        store = Store(base_path=args.base_path)

        # Run the command function
        args.func(store=store,
                  args=args)

    except KeymakerError as e:
        print(e.what, file=sys.stderr)

        sys.exit(1)


if __name__ == '__main__':
    main()
