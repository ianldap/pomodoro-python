# -*- mode: python ; coding: utf-8 -*-

# numpy, ssl e hashlib não são usados pelo timer. O pygame referencia numpy
# apenas em código de empacotamento que nunca é executado.
a = Analysis(
    ['pomodoro.py'],
    pathex=[],
    binaries=[],
    datas=[('alarme.mp3', '.'), ('pomodoro.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'ssl', '_ssl', '_hashlib', 'hashlib'],
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
    name='Pomodoro',
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
    icon=['pomodoro.ico'],
)
