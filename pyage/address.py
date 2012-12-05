from pyage.Inject import Inject

class AddressProvider(object):
    @Inject("population_generator")
    def __init__(self):
        super(AddressProvider, self).__init__()

    def generateAddress(self, obj):
        return "address:" + str(hash(obj))