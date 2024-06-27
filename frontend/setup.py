"""
Setup configuration for the ADGS Front-End application

module adgs
"""
from setuptools import setup, find_packages

setup(name="adgsfe",
      version="0.1.0",
      description="Front-End application for the Auxiliary Data Gathering Sevice (ADGS)",
      author="Daniel Brosnan",
      author_email="daniel.brosnan@deimos-space.com",
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3',
      install_requires=[
          "Flask",
          "Flask-DebugToolbar",
          "flask-security-too",
          "gunicorn",
          "requests"
      ],
      extras_require={
          "tests" :[
              "selenium"
          ]
      },
      test_suite='nose.collector')
