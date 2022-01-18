from setuptools import setup

install_requires = [
    'requests',
    'bs4',
]

packages = [
    'paizascraper',
]

setup(
    name='paizascraper',
    version='0.2',
    packages=packages,
    install_requires=install_requires,
    author='ryuma017',
)