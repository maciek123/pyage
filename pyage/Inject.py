
class Inject(object):
    def __init__(self, *args):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.args = args

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.


        about importing modules: http://docs.python.org/2/reference/simple_stmts.html#grammar-token-import_stmt
        """
        import conf as conf

        def wrapped_f(*args):
            for arg in self.args:
                setattr(args[0], arg, getattr(conf, arg))
            f(*args)

        return wrapped_f