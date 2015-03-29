from keymaker.commands import subparsers


def renew(store,
          args):
    host = store[args.host_name]

    host.renew()


renew.parser = subparsers.add_parser('renew',
                                     aliases=['update'],
                                     help='Renews an existing certificate')
renew.parser.set_defaults(func=renew)
renew.parser.add_argument(dest='host_name',
                          type=str,
                          metavar='NAME',
                          help='The host name')
