from distutils.core import setup

setup(
    name='Juju XaaS CLI',
    version='0.1.0',
    author='Justin SB',
    author_email='justin@fathomdb.com',
    packages=['jxaas'],
    url='http://pypi.python.org/pypi/jxaas/',
    license='LICENSE.txt',
    description='CLI for Juju XaaS.',
    long_description=open('README.md').read(),
    install_requires=[
        'jujuxaas'
    ],
    scripts=[
     'jxaas'
    ]
)