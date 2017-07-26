from distutils.core import setup, Extension

try:
    from Cython.Build import cythonize  # pylint: disable=W0611
    EXTENSIONS = [Extension('parsar.cparsar', ['parsar/cparsar.pyx'])]
except ImportError:
    EXTENSIONS = [Extension('parsar.cparsar', ['parsar/cparsar.c'])]

setup(
    name='parsar',
    packages=['parsar'],
    version='0.1.7',
    description='Python SAR data parser',
    author='Abe Friesen',
    author_email='abefriesen.af@gmail.com',
    url='https://github.com/doyshinda/parsar',
    license='MIT',
    ext_modules=EXTENSIONS,
    package_data={
        'parsar': [
            'cparsar.c'
        ]
    },
    keywords=['sar'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX :: Linux',

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
