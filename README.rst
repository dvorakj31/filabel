Introduction
============

This is simple console application, that labels your pull requests on github. Application can be started as flask app.

Installation
------------

1.  Install this module via pip - ``python -m pip install --extra-index-url https://test.pypi.org/pypi filabel_dvoraj84``.
2.  Install this module manually via github

    - Download repository
    - Unpack downloaded archive
    - Run ``python setup.py install``

Documentation
-------------
For documentation you have to build it on your own.

1. Install this module
2. Install requirements, that are stored in docs folder. ``pip install -r docs/requirements.txt``
3. ``cd docs``
4. ``make html`` - This will generate *_build/html/index.html* file.
5. ``make doctest`` to test documentation
