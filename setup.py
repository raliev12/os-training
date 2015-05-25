#!/usr/bin/env python

from setuptools import setup

setup(name='Pythonic Wrapper for Libvirt',
      version='1.0',
      author='Ruslan Aliev',
      author_email='raliev@mirantis.com',
      url='https://github.com/raliev12/os-training',
      py_modules=['libvirt_wrapper'],
      test_suite='libvirt_wrapper_test',
      )
