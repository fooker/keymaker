from setuptools import setup, find_packages

setup(
    name='keymaker',

    version='0.1',

    description='A management tool for SSL certificates and keys',
    url='https://github.com/fooker/keymaker/',

    author='Dustin Frisch',
    author_email='fooker@lab.sh',

    license='GPLv3',

    packages=find_packages(),

    install_requires=[
        'pyOpenSSL >= 0.14',
        'requests >= 2.0',
        'beautifulsoup4 >= 4.0'
    ],

    entry_points={
        'console_scripts': [
            'keymaker = keymaker.__main__:main'
        ],

        'keymaker.authorities': [
            'cacert = keymaker.authorities.cacert:CACert'
        ]
    }
)
