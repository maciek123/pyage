# coding=utf-8
from paver.easy import *
import paver.doctools
from paver.setuputils import setup

setup(
    name="PythonAgentBasedEvolution",
    packages=['pyage'],
    version="1.0",
    author="Maciej Kaziród",
    author_email="kmaciej@student.agh.edu.pl"
)


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass