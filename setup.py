import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'minimal', 'application.py')) as v_file:
    package_version = re.\
        compile(r".*__version__ = '(.*?)'", re.S).\
        match(v_file.read()).\
        group(1)


dependencies = [
    'restfulpy >= v2.6.9',
    'easycli',

    # deployment
    'gunicorn',

    # testing
    'bddrest >= v2.1.3'
]


setup(
    name="minimal",
    version=package_version,
    author="anonymous",
    author_email="arash.fattahzade@carrene.com",
    description="Minimal world",
    url='https://github.com/ArashFatahzade/bitwised-life.git',
    install_requires=dependencies,
    packages=find_packages(),
    test_suite="minimal.tests",
    entry_points={
        'console_scripts': [
            'minimal = minimal:minimal.cli_main'
        ]
    },
)
