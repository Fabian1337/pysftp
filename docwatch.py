#!/usr/bin/env python
"""A small utility to live build and reload in a webbrowser when a source or
config file changes. Very helpful for writing documentation."""

import platform
import webbrowser

from livereload import Server, shell


def main():
    """main routine"""
    make_cmd = 'make html'
    if platform.system() == 'FreeBSD':
        make_cmd = 'gmake html'
    server = Server()
    server.watch('docs/*.rst', shell(make_cmd, cwd='docs'))
    server.watch('pysftp/*.py', shell(make_cmd, cwd='docs'))
    webbrowser.open_new_tab('http://localhost:5500')
    server.serve(root='docs/_build/html', host='0.0.0.0')


if __name__ == '__main__':
    main()
