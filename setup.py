"""
Setup script for creating macOS application bundle using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['mdclick3.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'AppIcon.icns',  # Will be created by build script
    'plist': {
        'CFBundleName': 'Auto Mouse Clicker Pro',
        'CFBundleDisplayName': 'Auto Mouse Clicker Pro',
        'CFBundleGetInfoString': 'Professional Auto Mouse Clicker for macOS',
        'CFBundleIdentifier': 'com.amnasahamed.automouseclicker',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 Amnas Ahamed. All rights reserved.',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'LSMinimumSystemVersion': '10.14.0',  # macOS Mojave or later
        'NSAppleEventsUsageDescription': 'This app needs to control mouse clicks for automation.',
        'NSAppleScriptEnabled': False,
        # Request accessibility permissions
        'NSSystemAdministrationUsageDescription': 'This app needs accessibility permissions to control the mouse.',
    },
    'packages': ['tkinter', 'pyautogui', 'schedule'],
    'includes': ['json', 'os', 'time', 'threading', 'datetime', 'pathlib'],
    'excludes': [
        'matplotlib', 'numpy', 'pandas', 'scipy',  # Heavy packages
        'IPython', 'jupyter', 'notebook',  # Jupyter
        'pytest', 'test', 'tests',  # Testing
        'sphinx', 'docutils',  # Documentation
        'PIL.ImageQt', 'PIL.ImageTk',  # Unused PIL modules
        'black', 'pylsp',  # Development tools
        'multiprocessing', 'concurrent.futures',  # Not needed
        'rubicon',  # Problematic dependency
    ],
    'optimize': 2,  # Optimize bytecode
}

setup(
    name='Auto Mouse Clicker Pro',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'pyautogui>=0.9.53',
        'schedule>=1.1.0',
    ],
)
