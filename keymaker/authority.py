from abc import *

import pkg_resources


class AuthorityMeta(ABCMeta):
    def __getitem__(self,
                    name):
        for ep in pkg_resources.iter_entry_points(group='keymaker.authorities',
                                                  name=name):
            return ep.load()


class Authority(object,
                metaclass=AuthorityMeta):
    def __init__(self, store):
        self.__store = store

    @property
    def store(self):
        return self.__store

    @abstractmethod
    def create_crt(self, csr):
        pass

    @abstractmethod
    def renew_crt(self, serial):
        pass

    @abstractmethod
    def revoke_crt(self, serial):
        pass

    @abstractmethod
    def fetch_crt(self, serial):
        pass
