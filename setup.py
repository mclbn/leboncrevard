from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='leboncrevard',
    version='0.1.1',
    description='Python scrapper / mailer for the french ad website leboncoin.fr',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords='leboncoin scrapper',
    url='https://github.com/mclbn/leboncrevard',
    author='Marc Lebrun',
    # author_email='',
    license='ISC',
    packages=['leboncrevard'],
    install_requires=[
        'requests',
        'schedule',
        'beautifulsoup4',
    ],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    entry_points={
        'console_scripts': ['leboncrevard=leboncrevard.scheduler:main'],
    },
    include_package_data=True,
    zip_safe=False
)
