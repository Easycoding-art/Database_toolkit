from setuptools import setup
setup( 
	name='db_toolkit', 
	version='0.1', 
	description='Useful package to create database', 
	author='Easycoding-Art',
    packages=['db_toolkit'],
	install_requires=[ 
		'psycopg2', 
		'pandas',
        'faker',
        'wikipedia',
	], 
) 
