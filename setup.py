from setuptools import setup, find_packages
from os import path

setup(
	name='stableconfigs',
	version='1.0.0',
	description='A python package to find stable configurations for thermodynamic binding networks.',
	url='https://github.com/BensonKHuang/StableConfigs',
	author='Benson Huang, Hasan Saleemi, Varun Prabhu, Anthony Vento, Steven Wang, Kyle Zhou',
	author_email='BensonKHuang@gmail.com',
	
	# specifiy individual modules
	packages=find_packages(),
		
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',

		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	
	python_requires='>=3.6, <4',
	install_requires=['python-sat'],

	project_urls={
		'Bug Reports': 'https://github.com/BensonKHuang/StableConfigs/issues',
		'Source': 'https://github.com/BensonKHuang/StableConfigs',
	},
)

