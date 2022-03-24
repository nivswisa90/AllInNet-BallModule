from setuptools import setup, find_packages

setup(
    name='ballmodule',
    version='1.0.0',
    description='ballmodule',
    author='AllInNet',
    author_email='admin@allinnet.com',
    url='https://blog.godatadriven.com/setup-py',
    packages=find_packages(include=['ballmodule']),
    install_requires=[
        'requests~=2.27.1',
        'opencv-python~=4.5.5.62',
        'cvzone~=1.5.6',
        'numpy~=1.22.2'
    ]
)
