"""
Setup configuration for the adgsvboa application

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
from setuptools import setup, find_packages

setup(name="adgsboa",
      version="0.1.0",
      description="Engine and visualization tool for Business Operation Analysis",
      author="Daniel Brosnan",
      author_email="daniel.brosnan@deimos-space.com",
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3',
      install_requires=[
          "eboa",
          "vboa",
          "massedit"
      ],
      test_suite='nose.collector')
