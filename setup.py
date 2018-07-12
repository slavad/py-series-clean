# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

setup(
    name='pyclean',
    version='0.0.1',
    description='Python CLEAN implementation',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
       'numpy>=1.14.0<1.15.0'
    ]
    # TBD:
    #scripts=['scripts/pyclean', 'scripts/generate_test_seq']
    # TBD: dev, test etc
    # extras_require={
    # }
)