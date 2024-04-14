from setuptools import setup 

setup( 
	name='db_toolkit', 
	version='0.1', 
	description='A sample Python package', 
	author='John Doe', 
	author_email='jdoe@example.com',
    scripts=['db.py', 'fake_data.py'],  
	install_requires=[ 
		'psycopg2', 
		'pandas',
        'faker',
        'wikipedia',
	], 
) 
