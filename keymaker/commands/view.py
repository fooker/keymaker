from keymaker.commands import subparsers

from OpenSSL import crypto


def list(store,
         args):
    for host_name in store:
        print(host_name)

list.parser = subparsers.add_parser('list',
                                    help='Lists existing certificates')
list.parser.set_defaults(func=list)


def info(store,
         args):
    host = store[args.host_name]

    key = host.load_key()

    print('Private Key:')
    print('  Type = %s' % {crypto.TYPE_RSA: 'RSA',
                         crypto.TYPE_DSA: 'DSA'}[key.type()])
    print('  Size = %s' % key.bits())

    crt = host.load_crt()

    print('Certificate:')
    print('  Serial Number = %X' % crt.get_serial_number())
    print('  Version = %s' % crt.get_version())
    print('  Signature Algorithm = %s' % crt.get_signature_algorithm().decode('ascii'))
    print('  Issuer:')
    for k, v in crt.get_issuer().get_components():
        print('    %s = %s' % (k.decode('ascii'), v.decode('ascii')))
    print('  Subject')
    for k, v in crt.get_subject().get_components():
        print('    %s = %s' % (k.decode('ascii'), v.decode('ascii')))


info.parser = subparsers.add_parser('info',
                                    help='Prints details about a certificate ')
info.parser.set_defaults(func=info)
info.parser.add_argument(dest='host_name',
                         type=str,
                         metavar='NAME',
                         help='The host name')


def dump(store,
         args):
    host = store[args.host_name]

    if args.key:
        with host.key_path.open() as f:
            print(f.read().strip())

    if args.crt:
        with host.crt_path.open() as f:
            print(f.read().strip())


dump.parser = subparsers.add_parser('dump',
                                    help='Dumps a certificate')
dump.parser.set_defaults(func=dump)
dump.parser.add_argument(dest='host_name',
                         type=str,
                         metavar='NAME',
                         help='The host name')
dump.parser.add_argument('--key',
                         dest='key',
                         action='store_false',
                         default=True,
                         help='Show the private key')
dump.parser.add_argument('--crt',
                         dest='crt',
                         action='store_false',
                         default=True,
                         help='Show the certificate')

