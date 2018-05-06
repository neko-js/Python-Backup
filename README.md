# Backup Tool in Python

This package is used for creating backups of directories and/or files by calling a single command within Python.

The directories are backuped by creating uncompressed and password protected archives with 7-zip. The archive name will be the same name as the directory or file being backed up.

This package is only for MS Windows.

See below for an example.

## Installation

Installation is done via pip. Open command line and type in:
```
pip install git+https://github.com/smcgit/Python-Backup.git
```

To uninstall this package type in:
```
pip uninstall backup
```

## Usage

After importing the module, following command can be used to backup folders within Python environment:
```python
backup(paths_input, dir_output, pw)
```

* `paths_input` is a list of directories or files to backup.
* `dir_output` is an output directory for the 7z-files.
* `pw` is the password for the 7z-files.

An example is given as such (save this as another Python file):

```python
from backup import backup

# Specify input dirs/files and output directory here
paths_input = [
	'folder1',
	'../folder2',
	'C:/folder/file1.zip'
	]
dir_output = 'D:/Backup'

print('A password is needed for the backup files.')
pw = input('Enter a password: ')

backup(paths_input, dir_output, pw)

input('Press Enter to exit...')

```
