from keymaker.commands import subparsers


def dump(store,
         args):
    host = store[args.host_name]

    if not args.parts or 'key' in args.parts:
        with host.key_path.open() as f:
            print(f.read().strip())

    if not args.parts or 'crt' in args.parts:
        with host.crt_path.open() as f:
            print(f.read().strip())


dump.parser = subparsers.add_parser('dump',
                                    aliases=['show'],
                                    help='Dumps a certificate')
dump.parser.set_defaults(func=dump,
                         parts=[])
dump.parser.add_argument(dest='host_name',
                         type=str,
                         metavar='NAME',
                         help='The host name')
dump.parser.add_argument('--key',
                         dest='parts',
                         action='append_const',
                         const='key',
                         help='Show the private key')
dump.parser.add_argument('--crt',
                         dest='parts',
                         action='append_const',
                         const='crt',
                         default=True,
                         help='Show the certificate')

