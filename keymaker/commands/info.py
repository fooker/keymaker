from keymaker.commands import subparsers

from OpenSSL import crypto

import datetime


def info(store,
         args):
    host = store[args.host_name]

    key = host.load_key()

    print('Key:')
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
        print('    %-2s = %s' % (k.decode('ascii'), v.decode('ascii')))
    print('  Subject:')
    for k, v in crt.get_subject().get_components():
        print('    %-2s = %s' % (k.decode('ascii'), v.decode('ascii')))
    print('  Valid:')
    print('    Not Before = %s' % datetime.datetime.strptime(crt.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ'))
    print('    Not After  = %s' % datetime.datetime.strptime(crt.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ'))


info.parser = subparsers.add_parser('info',
                                    help='Prints details about a certificate ')
info.parser.set_defaults(func=info)
info.parser.add_argument(dest='host_name',
                         type=str,
                         metavar='NAME',
                         help='The host name')
