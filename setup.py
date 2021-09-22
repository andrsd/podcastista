from setuptools import setup
from podcastista import consts

setup(
    name='Podcastista',
    version=consts.VERSION,
    author='David Andrš',
    author_email='andrsd@gmail.com',
    url='https://github.com/andrsd/podcastista',
    license='LICENSE',
    description=consts.DESCRIPTION,
    install_requires=[
        'PyQt5==5.15.2',
        'pyaml==20.4.0',
        'spotipy==2.19.0',
        'Flask==2.0.1',
        'waitress==1.4.4',
        'python-dotenv>=0.15.0'
    ],
    packages=[
        'podcastista',
        'podcastista.assets',
    ],
    entry_points={
        'gui_scripts': [
            'podcastista = podcastista.__main__:main'
        ]
    },
    include_package_data=True,
    package_data={
        'podcastista.assets': ['*.svg']
    },
)
