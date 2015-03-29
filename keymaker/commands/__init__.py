from keymaker import parser


subparsers = parser.add_subparsers(title='Commands')


import keymaker.commands.view
import keymaker.commands.create
