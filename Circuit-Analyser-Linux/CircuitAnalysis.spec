# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['CircuitAnalysis.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/ccarter/Desktop/Circuit-Analysis-Calculator/icon.png', '.')],
    hiddenimports=['customtkinter', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='CircuitAnalysis',
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
    icon=['/home/ccarter/Desktop/Circuit-Analysis-Calculator/icon.png'],
)
