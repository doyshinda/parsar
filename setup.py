from distutils.core import setup

setup(
    name='parsar',
    packages=['parsar'],
    version='0.2.2',
    description='Python SAR data parser',
    author='Abe Friesen',
    author_email='abefriesen.af@gmail.com',
    url='https://github.com/doyshinda/parsar',
    license='MIT',
    keywords=['sar', 'sysstat'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'parsar = parsar.parsar:main',
        ],
    }
)
