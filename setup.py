from distutils.core import setup
from setuptools import find_packages

setup(
    name='parsar',
    packages=find_packages(),
    version='0.1.4',
    description='Python SAR data parser',
    author='Abe Friesen',
    author_email='abefriesen.af@gmail.com',
    url='https://github.com/doyshinda/parsar',
    license='MIT',
    package_data={
        'parsar': [
            'cparsar.so',
            'cparsar.cpython-34m.so'
        ]
    },
    keywords=['sar'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'parsar = parsar.parsar:main',
        ],
    }
)
