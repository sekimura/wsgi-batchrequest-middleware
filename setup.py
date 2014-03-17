from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.1'

setup(
      name='wsgi-batchrequest-middleware',
      version=version,
      description="This Wsgi middleware, for batch request",
      long_description=read('README.md'),
      classifiers=[
            "Development Status :: 4 - Beta",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
      ],
      keywords='wsgi middleware batch batchrequest',
      author='Masayoshi Sekimura',
      author_email='sekimura@gmail.com',
      url='https://github.com/sekimura/wsgi-batchrequest-middleware',
      license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      tests_require=['nose >= 0.11', 'mock', 'mako'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="tests",
      entry_points="""
      # -*- Entry points: -*-
      """,
)
