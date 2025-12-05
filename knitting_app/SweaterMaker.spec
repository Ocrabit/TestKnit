# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['runner.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/marcocassar/PycharmProjects/knitting_app/data/patterns/sizes/Pattern Sizes.json', 'data/patterns/sizes'),
    ('/Users/marcocassar/PycharmProjects/knitting_app/data/assets/icons', 'data/assets/icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SweaterMaker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/marcocassar/PycharmProjects/knitting_app/data/assets/app_icon/SweaterApp.icns'],
)
app = BUNDLE(
    exe,
    name='SweaterMaker.app',
    icon='/Users/marcocassar/PycharmProjects/knitting_app/data/assets/app_icon/SweaterApp.icns',
    bundle_identifier=None,
    distpath='/Users/marcocassar/PycharmProjects/knitting_app/build_folder/executable',
    workpath='/Users/marcocassar/PycharmProjects/knitting_app/build_folder/workpath',
)
