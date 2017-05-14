from distutils.core import setup
from setuptools import find_packages

setup(
    name='parsar',
    packages=find_packages(),
    version='0.1.3',
    description='Python SAR data parser',
    author='Abe Friesen',
    author_email='abefriesen.af@gmail.com',
    url='https://github.com/doyshinda/parsar',
    license='MIT',
    package_data={
        'parsar': ['cparsar.so']
    },
    keywords=['sar'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'parsar = parsar.parsar:main',
        ],
    }
)
