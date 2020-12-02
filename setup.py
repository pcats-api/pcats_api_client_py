from setuptools import setup

setup(
    name='pcats_api_client',
    url='https://github.com/pcats-api/pcatsAPIclientPy',
    author='Michal Kouril',
    author_email='michal.kouril@cchmc.org',
    packages=['pcats_api_client'],
    # Needed for dependencies
    # install_requires=['numpy'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='PCATS REST API Client',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)