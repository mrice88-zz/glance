import os
from setuptools import setup
from glance import __version__, __title__, __author__, __author_email__, __url__, __download_url__, __description__

readme_file_path = os.path.join('glance', 'readme.rst')

with open(readme_file_path, encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='glance_times',
    description=__description__,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    license='MIT License',
    url=__url__,
    download_url=__download_url__,
    keywords=['logging', 'utility'],
    packages=['glance'],
    package_data={__title__: [readme_file_path]},
    install_requires=['variants', 'attrs', 'python-dateutil'],
    classifiers=[]
)
