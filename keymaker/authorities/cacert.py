from keymaker.commands import KeymakerError
from keymaker.authority import Authority

import urllib

import requests
import bs4


class CACert(Authority):
    def __init__(self, store):
        super(CACert, self).__init__(store=store)

        # Get the certificate and key path and resolve it relative to the store location
        client_crt_path = self.store.base_path / self.config.get('client_crt', 'client.crt')
        if not client_crt_path.exists():
            raise KeymakerError('CACert client certificate not found: ' + str(client_crt_path))

        client_key_path = self.store.base_path / self.config.get('client_key', 'client.key')
        if not client_key_path.exists():
            raise KeymakerError('CACert client key not found: ' + str(client_key_path))

        # Create a session for HTTP requests
        self.__session = requests.Session()
        self.__session.cert = str(client_crt_path), str(client_key_path)
        self.__session.verify = '/etc/ssl/cert.pem'

    def __find_crt_id(self, serial):
        soup = bs4.BeautifulSoup(
            self.__session
            .get('https://secure.cacert.org/account.php?id=12')
            .content)

        crt_id = (
            urllib.parse.parse_qs(
                urllib.parse.urlparse(
                    soup
                    .find('td',
                          text='%06X' % serial)
                    .parent
                    .find('a')
                    ['href'])
                .query)
            ['cert']
            .pop())

        csrf = (
            soup
            .find('input',
                  attrs={'name': 'csrf'})
            ['value']
        )

        return crt_id, csrf

    def create_crt(self, csr):
        self.__session.post('https://secure.cacert.org/account.php',
                            data={'process': 'Submit',
                                  'oldid': 10,
                                  'description': 'Created by keymaker',
                                  'CSR': csr,
                                  'rootcert': 2,
                                  'hash_alg': 'sha256',
                                  'CCA': 'on'})

        return (
            bs4.BeautifulSoup(
                self.__session.post('https://secure.cacert.org/account.php',
                                    data={'oldid': 11,
                                          'process': 'Submit'})
                .content)
            .select('#content')
            .pop()
            .find('pre')
            .string
            .strip()
            .encode('ascii'))

    def renew_crt(self, serial):
        crt_id, csrf = self.__find_crt_id(serial)

        return (
            bs4.BeautifulSoup(
                self.__session
                .post('https://secure.cacert.org/account.php',
                      data={'renew': 'Renew',
                            'oldid': 12,
                            'revokeid[]': crt_id,
                            'csrf': csrf})
                .content)
            .select('#content')
            .pop()
            .find('pre')
            .string
            .strip()
            .encode('ascii'))

    def revoke_crt(self, serial):
        crt_id, csrf = self.__find_crt_id(serial)

        self.__session \
        .post('https://secure.cacert.org/account.php',
              data={'revoke': 'Revoke/Delete',
                    'oldid': 12,
                    'revokeid[]': crt_id,
                    'csrf': csrf})

    def fetch_crt(self, serial):
        crt_id, _ = self.__find_crt_id(serial)

        return (
            bs4.BeautifulSoup(
                self.__session
                .get('https://secure.cacert.org/account.php?id=15&cert=%d' % crt_id)
                .content)
            .select('#content')
            .pop()
            .find('pre')
            .string
            .strip()
            .encode('ascii'))
