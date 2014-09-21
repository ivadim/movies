import os, unittest

class BaseRestTest(unittest.TestCase):

    def load_fixture(self, path):
        curent_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(curent_dir, path)
        return open(path).read()