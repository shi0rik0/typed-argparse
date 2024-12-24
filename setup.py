from setuptools import setup, find_packages

setup(
    name='typed-argparse',
    version='0.0.3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='shi0rik0',
    description=
    'A wrapper around the standard library `argparse` with type hint support.',
    install_requires=['setuptools'],
    python_requires='>=3.8',
)
