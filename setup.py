from setuptools import setup, find_packages

setup(
    name='password-management-system',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A secure password management system with RESTful interfaces.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'bcrypt',  # For secure password hashing
        'requests'  # For making service calls to external APIs
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)