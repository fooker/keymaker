import pathlib as path

from OpenSSL import crypto

from keymaker.authority import Authority


class Host(object):
    def __init__(self,
                 store,
                 name):
        self.__store = store
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__store.base_path / self.__name

    @property
    def crt_path(self):
        return self.path / 'server.crt'

    @property
    def key_path(self):
        return self.path / 'server.key'

    @property
    def exists(self):
        return self.key_path.exists() and self.crt_path.exists()

    def load_crt(self):
        with self.crt_path.open('rb') as f:
            return crypto.load_certificate(crypto.FILETYPE_PEM,
                                           f.read())

    def load_key(self):
        with self.key_path.open('rb') as f:
            return crypto.load_privatekey(crypto.FILETYPE_PEM,
                                          f.read())

    def create(self):
        if self.exists:
            raise Exception('Certificate for host already exists')

        self.path.mkdir(mode=0o700)

        key = crypto.PKey()
        key.generate_key(type=crypto.TYPE_RSA,
                         bits=4096)

        key_data = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                          key)

        csr = crypto.X509Req()
        csr.get_subject().CN = self.name

        csr.set_pubkey(key)
        csr.sign(key, 'sha1')

        csr_data = crypto.dump_certificate_request(crypto.FILETYPE_PEM,
                                                   csr)

        crt_data = self.__store.authority.create_crt(csr_data)

        with self.key_path.open('wb') as f:
            f.write(key_data)

        with self.crt_path.open('wb') as f:
            f.write(crt_data)

    def renew(self):
        if not self.exists:
            raise Exception('Certificate for host does not exist')

        crt = self.load_crt()

        crt_data = self.__store.authority.renew_crt(serial=crt.get_serial_number())

        with self.crt_path.open('wb') as f:
            f.write(crt_data)

    def revoke(self):
        if not self.exists:
            raise Exception('Certificate for host does not exist')

        crt = self.load_crt()

        self.__store.authority.renew_crt(serial=crt.get_serial_number())

        self.crt_path.unlink()
        self.key_path.unlink()

        self.path.rmdir()


class Store(object):
    def __init__(self,
                 base_path):
        self.__base_path = path.Path(base_path)

        self.__authority = Authority(self)

    @property
    def base_path(self):
        return self.__base_path

    @property
    def authority(self):
        return self.__authority

    def __iter__(self):
        return (host_path.name
                for host_path
                in self.base_path.iterdir()
                if host_path.is_dir())

    def __getitem__(self, host_name):
        return Host(store=self,
                    name=host_name)
