from keymaker.commands import subparsers


def revoke(store,
           args):
    host = store[args.host_name]

    host.revoke()


revoke.parser = subparsers.add_parser('revoke',
                                      aliases=['delete'],
                                      help='Revokes and deletes an existing certificate')
revoke.parser.set_defaults(func=revoke)
revoke.parser.add_argument(dest='host_name',
                           type=str,
                           metavar='NAME',
                           help='The host name')
