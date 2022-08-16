import io
from setuptools import find_packages, setup

# Read in the README for the long description on PyPI
def long_description():
    with io.open('README.MD', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(name='core',
      version='0.1',
      description='description',
      long_description=long_description(),
      url='urls',
      author='Haeung',
      author_email='haeung@gist.ac.kr',
      license='free',
      packages=find_packages(),
      zip_safe=False)