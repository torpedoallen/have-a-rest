from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='have_a_rest',
      version=version,
      description="Way to RESTfully describe your API",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='REST API Python',
      author='torpedoallen',
      author_email='torpedoallen@gmail.com',
      url='https://github.com/torpedoallen/have-a-rest',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pytz',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
