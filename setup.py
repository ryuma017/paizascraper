from setuptools import setup

install_requires = [
    'requests',
    'bs4',
]

packages = [
    'paizascr',
]

setup(
    name='paizascr',
    version='0.1',
    packages=packages,
    install_requires=install_requires,
    author='Ryuma.T',
)