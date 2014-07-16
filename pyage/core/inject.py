config = None

#TODO refactor
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

        def wrapped_f(*args, **kwargs):
            conf = self.read_config(config)
            for arg in self.args:
                conf_arg_name = arg.split(":")[0]
                property_name = arg.split(":")[-1]
                try:
                    attr = getattr(conf, args[0].address.split('.')[0] + '__' + conf_arg_name)()
                except:
                    attr = getattr(conf, conf_arg_name)()
                setattr(args[0], property_name, attr)
            return f(*args, **kwargs)

        return wrapped_f


class InjectOptional(Inject):
    def __init__(self, *args):
        super(InjectOptional, self).__init__(*args)

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            try:
                conf = self.read_config(config)
                for arg in self.args:
                    conf_arg_name = arg.split(":")[0]
                    property_name = arg.split(":")[-1]
                    try:
                        attr = getattr(conf, args[0].address.split('.')[0] + '__' + conf_arg_name)()
                    except:
                        attr = getattr(conf, conf_arg_name)()
                    setattr(args[0], property_name, attr)
            except:
                pass #parameter is not mandatory
            return f(*args, **kwargs)

        return wrapped_f


class Singleton(object):
    def __init__(self, f):
        self.result = None

    def __call__(self, f):
        if not self.result:
            self.result = f()
        return self.result

