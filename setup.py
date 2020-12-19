from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, './fingerprintweb/__version__.py'), encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name='fingerprintweb',
    version=version,
    description='A tool for detecting technologies used by web applications. Hard forks wad v0.4.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/0xcrypto/fingerprints',
    license='GPLv3',
    author='0xcrypto',
    author_email='vi@hackberry.xyz',
    packages=find_packages(),
    include_package_data=True,
    requires=['six'],
    install_requires=['six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={
        'console_scripts': [
            'fingerprint = fingerprintweb.__main__:main'
        ]
    },
)
