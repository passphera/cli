import os
import sys
from setuptools import setup, find_packages

app_path = os.path.join(os.path.dirname(__file__), "app")
sys.path.insert(0, app_path)

from core.constants import APP

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=APP.NAME,
    version=APP.VERSION,
    author=APP.AUTHOR,
    author_email=APP.AUTHOR_EMAIL,
    url=APP.URL,
    license=APP.LICENSE,
    description=APP.DESCRIPTION,
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
