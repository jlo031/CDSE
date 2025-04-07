import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name = "CDSE",
    version = "0.0.0",
    author = "Johannes Lohse",
    author_email = "johannes.lohse@uit.no",
    description = ("Search and download data from CDSE."),
    license = "The Ask Johannes Before You Do Anything License",
    long_description=read('README.md'),
    install_requires = [
        'loguru',
        'requests',
        'geojson',
        'geomet',
        'python-dotenv',
        'pathlib',
        'ipython',
    ],
    packages = find_packages(where='src'),
    package_dir = {'': 'src'},
    package_data = {'': ['*.xml']},
    entry_points = {
        'console_scripts': [
        ]
    },
    include_package_data=True,
)
