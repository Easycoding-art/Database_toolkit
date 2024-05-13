from setuptools import setup, find_packages
setup(
    name='db_toolkit', 
	version='1.0', 
	description='Useful package to create database', 
	author='Easycoding-Art',
    packages=find_packages(),
	install_requires=[ 
		'psycopg2', 
		'pandas',
        'faker',
        'wikipedia'
	],
    py_modules=["parser_file"],
    include_package_data=True
) 
