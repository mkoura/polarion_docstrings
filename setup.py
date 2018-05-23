# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='polarion-docstrings',
    packages=find_packages(),
    entry_points={
        'flake8.extension': [
            'P66 = polarion_docstrings.checker:polarion_checks492',
        ],
    },
    keywords=['polarion', 'testing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers'],
    include_package_data=True
)
