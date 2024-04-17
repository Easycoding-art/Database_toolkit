from setuptools import setup 

setup( 
	name='db_toolkit', 
	version='0.1', 
	description='Useful package to create database', 
	author='Easycoding-Art',
    scripts=['db.py', 'fake_data.py'],
    py_modules=[], 
	install_requires=[ 
		'psycopg2', 
		'pandas',
        'faker',
        'wikipedia',
	], 
) 
