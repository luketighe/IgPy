#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.build_py import build_py as build_py

setup(cmdclass={'build_py': build_py},
      name='IgPy',
      version="0.0.1",
      description='IG Labs REST & Streaming API',
      author='Luke Tighe',
      author_email='luke.tighe@outlook.com',
      url='https://github.com/luketighe/IgPy',
      license='BSD License',
      packages=['igpy'],
      platforms=['3.5.*'],
      install_requires=[
          'requests',
      ],
    )