import os

import PyInstaller.__main__
import foodcalendar

PyInstaller.__main__.run([
    '--name=fs_calendar.exe',
    '--onefile',
    '--windowed',
    '--add-data=%s' %'fs.ico',
    '--icon=%s' %'fs.ico',
    'foodcalendar.py',
])