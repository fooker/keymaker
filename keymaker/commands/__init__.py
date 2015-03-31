from keymaker import parser


subparsers = parser.add_subparsers(title='Commands')


class KeymakerError(Exception):
    def __init__(self, what):
        super(KeymakerError, self).__init__()

        self.what = what


import keymaker.commands.create
import keymaker.commands.dump
import keymaker.commands.info
import keymaker.commands.list
import keymaker.commands.renew
import keymaker.commands.revoke
