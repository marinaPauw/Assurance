# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\newMarina\\Desktop\\Assurance\\Assurance.py'],
             pathex=['C:\\Users\\newMarina\\Desktop\\Assurance'],
             binaries=[],
             datas=[('C:\\Users\\newMarina\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\sklearn\\.libs\\vcomp140.dll', '.')],
             hiddenimports=['sklearn.utils._cython_blas', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Assurance',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='C:\\Users\\newMarina\\Desktop\\Assurance\\assurance.ico')
