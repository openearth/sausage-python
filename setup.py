from setuptools import setup, find_packages

setup(
    name='sausage',
    version='0.1.0',
    description='Toolbox to convert numerical geophisical model input and output',
    author = 'Bas Hoonhout',
    author_email='bas.hoonhout@deltares.nl',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'xarray',
        'docopt',
        'six',
    ],
    tests_require=[
        'nose'
    ],
    test_suite='nose.collector',
    entry_points={'console_scripts': [
        'sausage-convert = sausage.console:convert',
        'sausage-compile = sausage.console:compile',
    ]},
)
