import urllib

import requests
import bs4


class Authority(object):
    def __init__(self, store):
        self.__store = store

        self.__session = requests.Session()
        self.__session.cert = (str(store.base_path / '.client.crt'),
                               str(store.base_path / '.client.key'))

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
        pass

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
