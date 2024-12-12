from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='passphera',
    version='1.1.0',
    author='Fathi Abdelmalek',
    url='https://github.com/passphera/cli',
    license='Apache-2.0',
    author_email='passphera@gmail.com',
    description='Strong passwords generator and manager',
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
