from setuptools import setup, find_packages

kwargs = {
    # Packages
    'packages': find_packages(),
    'include_package_data': True,

    'test_suite': 'tests',

    # Metadata
    'name': 'pipes',
    'version': __import__('pipes').get_version(),
    'author': 'Byron Ruth',
    'author_email': 'b@devel.io',
    'description': 'Iterator-based utilities for building data processing pipelines',
    'license': 'BSD',
    'keywords': 'pipeline data processing iterator merge compose',
    'url': 'https://github.com/bruth/pipes/',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
    ],
}

setup(**kwargs)
