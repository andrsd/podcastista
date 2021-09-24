# -*- mode: python ; coding: utf-8 -*-

import os
from os.path import join
import sys
from podcastista import consts

block_cipher = None


a = Analysis(
    [join('podcastista', '__main__.py')],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        ('.env', '.'),
        (join('podcastista', 'assets', 'icons', '*.svg'), 'icons')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=consts.APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None)

if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name=f'{consts.APP_NAME}.app',
        icon=None,
        bundle_identifier='name.andrs.osx.podcastista',
        version=f'{consts.VERSION}',
        info_plist={
            'CFBundleGetInfoString': f'{consts.DESCRIPTION}',
            'NSHumanReadableCopyright': f'{consts.COPYRIGHT}'
        }
    )
