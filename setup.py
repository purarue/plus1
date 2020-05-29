#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = []

setup(
    author="Sean Breckenridge",
    author_email='seanbrecke@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requirements,
    license="MIT",
    include_package_data=True,
    name='plus1',
    packages=find_packages(include=['plus1']),
    entry_points = {
        'console_scripts': [
            "plus1 = plus1.plus1:main"
        ]
    },
    url='https://gitlab.com/seanbreckenridge/plus1',
    version='0.1.0',
    zip_safe=False,
)
