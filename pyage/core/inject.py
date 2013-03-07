
config = None

class Inject(object):
    def __init__(self, *args):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.args = args

    def read_config(self, config):
        # about importing modules: http://docs.python.org/2/reference/simple_stmts.html#grammar-token-import_stmt
        exec "import " + config + " as conf"
        return conf

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process!

        """

        def wrapped_f(*args):
            conf = self.read_config(config)
            for arg in self.args:
                setattr(args[0], arg, getattr(conf, arg)())
            f(*args)

        return wrapped_f


class Singleton(object):
    def __init__(self, f):
        self.result = None

    def __call__(self, f):
        if not self.result:
            self.result = f()
        return self.result

