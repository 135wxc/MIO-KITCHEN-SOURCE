#!/usr/bin/env python3
# pylint: disable=line-too-long
import os
import platform
import shutil
import zipfile
from platform import system, machine
from pip._internal.cli.main import main as _main
with open('requirements.txt', 'r', encoding='utf-8') as l:
    for i in l.read().split("\n"):
        print(f"Installing {i}")
        _main(['install', i])
ostype = system()
if ostype == 'Linux':
    name = 'MIO-KITCHEN-linux.zip'
elif ostype == 'Darwin':
    name = 'MIO-KITCHEN-macos.zip'
    try:
        from tkinter import END
    except:
        print("Tkinter IS not exist!\nThe Build may not Work!")
else:
    name = 'MIO-KITCHEN-win.zip'


def zip_folder(folder_path):
    # 获取文件夹的绝对路径和文件夹名称
    abs_folder_path = os.path.abspath(folder_path)

    # 创建一个同名的zip文件
    zip_file_path = os.path.join(local, name)
    archive = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)

    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(abs_folder_path):
        for file in files:
            if file == name:
                continue
            file_path = os.path.join(root, file)
            if ".git" in file_path:
                continue
            print(f"Adding: {file_path}")
            # 将文件添加到zip文件中
            archive.write(file_path, os.path.relpath(file_path, abs_folder_path))

    # 关闭zip文件
    archive.close()
    print("Done!")


local = os.getcwd()
print("Building...")
import PyInstaller.__main__
if ostype == 'Darwin':
    PyInstaller.__main__.run([
        'tool.py',
        '-Fw',
        '--exclude-module',
        'numpy',
        '-i',
        'icon.ico',
        '--collect-data',
        'sv_ttk',
        '--collect-data',
        'chlorophyll',
        '--hidden-import',
        'tkinter',
        '--hidden-import',
        'PIL',
        '--hidden-import',
        'PIL._tkinter_finder'
    ])
elif os.name == 'posix':
    PyInstaller.__main__.run([
        'tool.py',
        '-Fw',
        '--exclude-module',
        'numpy',
        '-i',
        'icon.ico',
        '--collect-data',
        'sv_ttk',
        '--collect-data',
        'chlorophyll',
        '--hidden-import',
        'tkinter',
        '--hidden-import',
        'PIL',
        '--hidden-import',
        'PIL._tkinter_finder',
        '--splash',
        'splash.png'
    ])
elif os.name == 'nt':
    PyInstaller.__main__.run([
        'tool.py',
        '-Fw',
        '--exclude-module',
        'numpy',
        '-i',
        'icon.ico',
        '--collect-data',
        'sv_ttk',
        '--collect-data',
        'chlorophyll',
        '--splash',
        'splash.png'
    ])
if not os.path.exists('dist/bin'):
    os.makedirs('dist/bin', exist_ok=True)
pclist = ['images', 'languages', 'licenses', 'module', 'temp', 'extra_flash.zip', 'setting.ini', ostype]
for i in os.listdir(local + os.sep + "bin"):
    if i in pclist:
        if os.path.isdir(f"{local}/bin/{i}"):
            shutil.copytree(f"{local}/bin/{i}", f"{local}/dist/bin/{i}", dirs_exist_ok=True)
        else:
            shutil.copy(f"{local}/bin/{i}", f"{local}/dist/bin/{i}")
if not os.path.exists('dist/LICENSE'):
    shutil.copy(f'{local}/LICENSE', local + os.sep + "dist" + os.sep+'LICENSE')
if os.name == 'posix':
    if platform.machine() == 'x86_64' and os.path.exists(f'{local}/dist/bin/Linux/aarch64'):
        try:
            shutil.rmtree(f'{local}/dist/bin/Linux/aarch64')
        except:
            pass
    for root, dirs, files in os.walk(local + os.sep + 'dist', topdown=True):
        for i in files:
            print(f"Chmod {os.path.join(root, i)}")
            os.system(f"chmod a+x {os.path.join(root, i)}")
os.chdir(f'{local}/dist')
zip_folder(".")
