from setuptools import setup, find_packages
setup( 
	name='db_toolkit', 
	version='0.1', 
	description='Useful package to create database', 
	author='Easycoding-Art',
    packages=find_packages(where='db_toolkit'),
    package_dir={'': 'db_toolkit'}, 
	install_requires=[ 
		'psycopg2', 
		'pandas',
        'faker',
        'wikipedia',
	], 
) 
