from setuptools import setup
from setuptools import find_packages


from lws import version


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
  name='lws',
  version=str(version.version),
  description='Logfile Warning Suppressor',
  long_description=readme(),
  classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'Programming Language :: Python :: 3',
      'Intended Audience :: End Users/Desktop',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Operating System :: POSIX :: Linux',
      'Topic :: Software Development :: Quality Assurance',
      'Topic :: Text Processing :: General',
  ],
  url='https://github.com/jeremiah-c-leary/logfile-warning-suppressor',
  download_url='https://github.com/jeremiah-c-leary/logfile-warning-suppressor',
  author='Jeremiah C Leary',
  author_email='jeremiah.c.leary@gmail.com',
  license='GNU General Public License',
  packages=find_packages(),
  zip_safe=False,
  test_suite='nose.collector',
  tests_require=['nose'],
  keywords=['eda', 'warning', 'suppression', 'logfile'],
  install_requires=[
    'PyYAML'
  ],
  entry_points={
    'console_scripts': [
      'lws = lws.__main__:main'
    ]
  }
)
