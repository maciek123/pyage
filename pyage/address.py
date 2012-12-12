
class AddressProvider(object):
    def __init__(self):
        super(AddressProvider, self).__init__()

    def generateAddress(self, obj):
        return "address:" + str(hash(obj))