
"""
A setuptools based setup module.

"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Kent Energy Data',
    version='0.1.0',
    description='Web scraping and database storage',
    long_description=long_description,
    author='Andrew Moss',
    author_email='agordonmoss@gmail.com',
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
        keywords='web scraping',
        url='https://github.com/agmoss',
        license=license,
        packages=find_packages(exclude=('tests', 'docs'))
)