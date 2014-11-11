from unittest import TestCase

from pyage.core import inject

from pyage.core.inject import Inject, InjectWithDefault


class TestClass(object):
    @Inject("stats")
    @InjectWithDefault(("foo", 4))
    def __init__(self):
        super(TestClass, self).__init__()


class TestInject(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestInject, cls).setUpClass()
        inject.config = "pyage.conf.test_conf"

    def test_inject(self):
        t = TestClass()
        self.assertTrue(hasattr(t, "stats"))
        self.assertEqual(t.foo, 4)