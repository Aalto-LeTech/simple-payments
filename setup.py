#!/usr/bin/env python3
import re
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

def read_requirements(filename='requirements.txt'):
    with open(path.join(here, filename), encoding='utf-8') as f:
        return list(filter(None, (
            line.split('#', 1)[0].strip() for line in f.read().splitlines()
        )))
    return []

def find_version(*file_paths):
    with open(path.join(here, *file_paths), 'r') as fp:
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", fp.read(), re.M)
        if match:
            return match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='simple-payments',
    version=find_version('payments', '__init__.py'),
    description="A Flask project implementing a dummy payment service for educational use.",
    long_description=long_description,
    url='https://github.com/Aalto-LeTech/simple-payments',
    author='Jaakko Kantojärvi',
    author_email='jaakko@n-1.fi',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Education',
        'Operating System :: OS Independent',

        'Environment :: Web Environment',
        'Framework :: Flask',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],

    zip_safe=False,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,

    install_requires=read_requirements(),
    extras_require={
        'prod': read_requirements('requirements_prod.txt'),
    },
)
