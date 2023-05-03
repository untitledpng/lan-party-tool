import os
import shutil
import win32com.client

# Get the path of the current directory
current_dir = os.getcwd()

# Get the path of the Windows user startup folder
startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

# Create a shortcut to the file in the startup folder
shortcut_name = 'MyShortcut.lnk'
shortcut_path = os.path.join(startup_folder, shortcut_name)
target_path = os.path.join(f"{current_dir}\stable", 'GooseDesktop.exe')
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = target_path
shortcut.WindowStyle = 1
shortcut.save()