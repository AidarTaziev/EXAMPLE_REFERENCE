from setuptools import setup, find_packages


setup(
    name="django-sso-client",
    version='0.0.6',
    description="SSO for django client app",
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django sso',
    author='Ferma',
    author_email='bloq98@gmail.com',
    url='https://github.com/ferma666/sso_auth_module',
    packages=find_packages(),
    install_requires=[
        'Django>=2.1',
    ],
    include_package_data=True,
    zip_safe=False,
)
