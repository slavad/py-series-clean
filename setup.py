# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-series-clean',
    version='0.0.1',
    description='Python CLEAN implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/slavad/py-series-clean',
    author='Viacheslav Dushin',
    keywords='time series analysis, CLEAN algorithm',
    packages=find_packages(),
    classifiers=[
        #TODO: test with other versions
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
       'numpy>=1.14.0<1.15.0'
    ]
    # TBD:
    #scripts=['scripts/pyclean', 'scripts/generate_test_series']
    # TBD: dev, test etc
    # extras_require={
    # }
)