# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['chain_PDFs_deep.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\jmonti\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\tkinterdnd2\\tkdnd', 'tkinterdnd2\\tkdnd')],
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
    name='chain_PDFs_deep',
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
)
