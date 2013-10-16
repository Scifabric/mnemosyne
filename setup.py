from setuptools import setup, find_packages
try:
    requirements = open('requirements.txt').read().split('\n')
except:
    requirements = []

setup(
    name='pybossa-links',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    author='Daniel Lombraña González',
    author_email='teleyinex@gmail.com',
    description='Web module for storing image links',
    long_description='''PyBossa-links is a web service that saves image links,
                        analyze them, and create tasks in a PyBossa server''',
    license='AGPLv3',
    url='https://github.com/teleyinex/pybossa-links',
    download_url='https://github.com/teleyinex/pybossa-links',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
    '''
)
