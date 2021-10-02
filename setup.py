from setuptools import setup
from podcastista import consts
from glob import glob
import platform

main_script = 'podcastista/__main__.py'
assets_dir = 'podcastista/assets'

if platform.system() == 'Darwin':
    PLIST_INFO = {
        'CFBundleName': consts.APP_NAME,
        'CFBundleDisplayName': consts.APP_NAME,
        'CFBundleGetInfoString': consts.DESCRIPTION,
        'CFBundleIdentifier': "name.andrs.osx.podcastista",
        'CFBundleVersion': str(consts.VERSION),
        'CFBundleShortVersionString': str(consts.VERSION),
        'NSHumanReadableCopyright': consts.COPYRIGHT
    }

    extra_options = dict(
        setup_requires=['py2app'],
        app=[main_script],
        data_files=[
            ('icons', glob(assets_dir + '/icons/*.svg')),
            ('', ['podcastista/.env'])
        ],
        options={
            'py2app': {
                'argv_emulation': False,
                'plist': PLIST_INFO
            }
        }
    )
elif platform.system() == 'win32':
     extra_options = dict(
         setup_requires=['py2exe'],
         app=[mainscript],
     )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install" and install
        # the main script as such
        scripts=[main_script]
    )

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
    **extra_options
)
