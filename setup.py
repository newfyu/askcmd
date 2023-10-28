from setuptools import setup, find_packages

setup(
    name="askcmd",
    version="0.1.1",
    author='lhan',
    author_email='lhan12345@hotmail.com',
    description='A command line tool to generate any commands from natural language',
    packages=find_packages(),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'askcmd = askcmd.__main__:main',
        ],
    }
)
