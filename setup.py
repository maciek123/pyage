# coding=utf-8
from distutils.core import setup
from setuptools import find_packages

setup(
    name="pyage",
    description="Python Agent-based evolution",
    packages=find_packages(),
    version="1.2.11",
    author="Maciej Kaziród",
    author_email="kazirod.maciej@gmail.com",
    requires=['Pyro4(==4.17)']
)

