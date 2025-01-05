import os
import sys
from setuptools import setup, find_packages

app_path = os.path.join(os.path.dirname(__file__), "app")
sys.path.insert(0, app_path)

from core.config import (
    __name__, __version__, __author__, __author_email__, __url__, __license__, __copyright__, __description__
)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    copyright=__copyright__,
    description=__description__,
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'passphera=app.entrypoint:main',
        ]
    }
)
