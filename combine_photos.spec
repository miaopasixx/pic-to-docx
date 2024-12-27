# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

block_cipher = None

# 添加版本信息
version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),    # 文件版本号 (1.0.0.0)
        prodvers=(1, 0, 0, 0),    # 产品版本号
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                '080404b0',  # 中文编码
                [StringStruct('CompanyName', '个人开发'),
                 StringStruct('FileDescription', '照片合并工具 - 自动将活动照片合并为Word文档'),
                 StringStruct('FileVersion', '1.0.0.0'),
                 StringStruct('InternalName', 'combine_photos'),
                 StringStruct('LegalCopyright', 'Copyright (C) 2024'),
                 StringStruct('OriginalFilename', '活动图片转word.exe'),
                 StringStruct('ProductName', '活动图片转word'),
                 StringStruct('ProductVersion', '1.0.0.0')])
        ]),
        VarFileInfo([VarStruct('Translation', [2052, 1200])])  # 中文语言代码
    ]
)

a = Analysis(
    ['combine_photos.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='活动图片转word',
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
    entitlements_file=None,
    icon='photo.ico',
    version=version_info  # 添加版本信息
)