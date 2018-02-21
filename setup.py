from distutils.core import setup
setup(
    name='xmlcomparator',
    packages=['xmlcomparator'],  # this must be the same as the name above
    # https://packaging.python.org/tutorials/distributing-packages/#pre-release-versioning
    version='0.1a1',
    description='A flexible xml comparator',
    author='Andrii Kozin',
    author_email='z4i.andrey@gmail.com',
    # use the URL to the github repo
    url='https://github.com/andrii-z4i/xml-comparator',
    download_url='https://github.com/andrii-z4i/xml-comparator/archive/0.1.tar.gz',
    license='gpl-3.0',
    keywords=['xml', 'diff', 'flexible'],  # arbitrary keywords
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Xml Diff',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3.0 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6'
)
