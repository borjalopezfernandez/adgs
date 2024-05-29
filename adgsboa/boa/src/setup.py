"""
Setup configuration for the naosvboa application

Written by DEIMOS Space S.L. (dibb)

module naosboa
"""
from setuptools import setup, find_packages

setup(name="naosboa",
      version="0.1.5",
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
