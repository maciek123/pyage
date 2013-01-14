import sys
from pyage import inject
from pyage.Computation import Computation

if __name__ == '__main__':
    inject.config = sys.argv[1]
    computation = Computation()
    computation.run()
