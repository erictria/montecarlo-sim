from setuptools import setup

setup(
    name = 'Montecarlo Simulator',
    version = '1.0',
    description = 'A package that implements a simple Monte Carlo simulator using a set of related classes',
    url = 'https://github.com/erictria/montecarlo-sim',
    author = 'Eric Tria',
    author_email = 'ericmtria@gmail.com',
    license = 'MIT',
    packages = ['montecarlo'],
    requires = ['pandas', 'unittest']
)