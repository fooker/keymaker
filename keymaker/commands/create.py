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


def renew(store,
          args):
    host = store[args.host_name]

    host.renew()


renew.parser = subparsers.add_parser('renew',
                                     help='Renews an existing certificate')
renew.parser.set_defaults(func=renew)
renew.parser.add_argument(dest='host_name',
                          type=str,
                          metavar='NAME',
                          help='The host name')
