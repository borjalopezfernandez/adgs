"""
Setup configuration for the AUXIP application

module auxip
"""
from setuptools import setup, find_packages

setup(name="auxip",
      version="0.0.1",
      description="Auxiliary Data Gathering Service Interface Point",
      author="Borja López Fernández",
      author_email="borja.lopez@deimos-space.com ",
      packages=find_packages(),
      python_requires='>=3',
      install_requires=[
          "sqlalchemy",
          "sqlalchemy_guid",
          "sqlmodel",
          "psycopg2",
          "psycopg2-binary",
          "alembic",
          "fastapi[all]",
          "httpx",
          "requests"
      ],
      extras_require={
          "tests" :[
              "pytest"
          ]
      }
)
