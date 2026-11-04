# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['pac-man.py'],
    datas=[('assets', 'assets'), ('config.json', '.'), ('HOW_TO_PLAY.txt', '.')],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='pac-man',
    upx=True,
    console=True,
)

coll = COLLECT(
    exe, a.binaries, a.datas,
    upx=True,
    name='pac-man',
)
