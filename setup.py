from setuptools import setup

setup(
    name='pcats_api_client',
    url='https://github.com/pcats-api/pcats_api_client_py',
    author='Michal Kouril',
    author_email='michal.kouril@cchmc.org',
    packages=['pcats_api_client'],
    # Needed for dependencies
    install_requires=['requests'],
    # *strongly* suggested for sharing
    version='1.1.0',
    # The license can be anything you like
    license='MIT',
    description='PCATS REST API Client',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    long_description=open('README.md').read(),
    include_package_data=True,
)
