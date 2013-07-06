import os

from jinja2 import nodes
from jinja2.ext import Extension


class StaticExtension(Extension):
    tags = set(['static'])

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        if parser.stream.current.type == 'block_end':
            filename = ''
        else:
            filename = next(parser.stream).value
        node = nodes.Const(self.get_static_path(filename))

        return node

    def get_static_path(self, filename=None):
        if filename is None:
            filename = ''

        return os.path.join('/', self.static_path, filename)


def static(static_path):
    StaticExtension.static_path = static_path
    return StaticExtension
