#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <mail@fabienm.eu>
# Created:  14/10/2019
#-----------------------------------------------------------------------------
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cocomod-spi",
    use_scm_version={
        "relative_to": __file__,
        "write_to": "cocomod/spi/version.py",
    },
    author="Fabien Marteau",
    author_email="mail@fabienm.eu",
    description="Cocotb SPI module",
    long_description=long_description,
    url="https://github.com/Martoni/cocomod-spi.git",
    packages=["cocomod.spi"],
    install_requires=['cocotb'],
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)


