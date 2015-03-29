from keymaker.commands import subparsers


def create(store,
           args):
    host = store[args.host_name]

    host.create()


create.parser = subparsers.add_parser('create',
                                      help='Creates a new certificate')
create.parser.set_defaults(func=create)
create.parser.add_argument(dest='host_name',
                           type=str,
                           metavar='NAME',
                           help='The host name')
