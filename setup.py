from setuptools import setup, find_packages


setup(
    name='corvus',
    version='0.0.8',
    url='https://github.com/OlenEnkeli/corvus',
    packages=find_packages(),
    license='BSD',
    author='Anton Niksolkiy',
    author_email='angeloffree@yandex.ru',
    description='Python WebSocket framework with JSON-RPC implementation',
    data_files=[('', ['LICENSE.md'])],
    install_requires=[
        'uvicorn',
        'uvloop',
        'marshmallow',
        'websockets'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=True
)
