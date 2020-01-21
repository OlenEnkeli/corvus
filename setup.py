from setuptools import setup, find_packages


setup(
    name='corvus',
    version='0.0.1',
    url='https://github.com/OlenEnkeli/corvus',
    packages=find_packages(),
    license='BSD',
    author='Anton Niksolkiy',
    author_email='angeloffree@yandex.ru',
    description='Python WebSocket framework with JSON-RPC implementation',
    data_files=[('', ['LICENSE.md'])],
    extras_require={
        'full': [
            'uvicorn',
            'uvloop',
            'marshmallow',
            'websockets'
        ]
    },
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WebSocket',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False
)
