from setuptools import setup, find_packages


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='filabel_dvoraj84',
    version='0.3',
    description='Labels pull requests on github',
    long_description=long_description,
    author='Jakub Dvořák',
    author_email='dvoraj84@fit.cvut.cz',
    license='MIT',
    url='https://github.com/dvorakj31/filabel',
    packages=find_packages(),
    keywords=['pull requests', 'github', 'labeling', 'flask', 'console'],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=[
        'click',
        'colorama',
        'Flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'filabel = filabel:main',
        ]
    },
    package_data={
        'filabel': [
            'templates/*.html',
        ]
    },
    zip_safe=False,
)
