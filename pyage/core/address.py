import os
import socket
from pyage.core.inject import Inject

class AddressProvider(object):
    def generate_address(self, obj):
        raise NotImplementedError()

counter = 0

class SequenceAddressProvider(AddressProvider):
    def __init__(self):
        super(SequenceAddressProvider, self).__init__()

    def generate_address(self, obj):
        global counter
        counter += 1
        return str(counter) + "." + socket.gethostname() + "." + str(os.getpid())

class Addressable(object):
    @Inject("address_provider")
    def __init__(self):
        super(Addressable, self).__init__()
        if hasattr(self, "name") and self.name:
            self.address = self.name + "." + socket.gethostname() + "." + str(os.getpid())
        else:
            self.address = self.address_provider.generate_address(self)

    def get_address(self):
        return self.address