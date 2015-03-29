from keymaker import parser


subparsers = parser.add_subparsers(title='Commands')


import keymaker.commands.create
import keymaker.commands.dump
import keymaker.commands.info
import keymaker.commands.list
import keymaker.commands.renew
import keymaker.commands.revoke
