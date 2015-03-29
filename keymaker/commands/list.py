from keymaker.commands import subparsers


def list(store,
         args):
    for host_name in store:
        print(host_name)

list.parser = subparsers.add_parser('list',
                                    help='Lists existing certificates')
list.parser.set_defaults(func=list)
