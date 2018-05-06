import subprocess
from math import log, floor
from os import stat, rename, remove
from pathlib import Path
from time import time, strftime

def example():
    '''
    This script is used for creating backups of the files and folders listed in paths_input.
    This is done by creating an uncompressed and password protected 7-zip archive for each element in paths_input.
    The existing archive will be overwritten, if the script is called a second time. This is faster than updating the 7z file, since a large number of files are involved during a backup process.
    '''
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


def backup(paths_input, dir_output, pw):
    print('Running Backup Script...\n')
    time_start_total = time()
    
    for path_input in paths_input:

        # Get filename from input path
        file_name = Path(path_input).stem
        if any(file_name is x for x in ('.', '..')):
            file_name = 'Backup.7z'
        else:
            file_name = file_name + '.7z'
        
        # Normalized paths
        path_input = str(Path(path_input))
        path_output = str(Path(dir_output) / file_name) 

        # If 7z-file already exists rename it to .tmp (delete any other tmp file before)
        path_output_tmp = path_output + '.tmp'
        if Path(path_output).is_file():
            if Path(path_output_tmp).is_file():
                print('Removing old temporary file:', path_output_tmp)
                remove(path_output_tmp)
            print('Creating temporary file of current backup:', path_output_tmp)
            rename(path_output, path_output_tmp)
        
        print('Started: ', strftime('%H:%M:%S'))
        print('Creating for: ', path_input)
        time_start = time()
        
        # Zip it
        success = zip(path_input, path_output, pw)

        # If zip operation was successful and tmp file exists, remove tmp file
        if Path(path_output_tmp).is_file():
            if success:
                print('Successful backup! Removing old backup:', path_output_tmp)
                remove(path_output_tmp)
            else:
                print('Temporary file of old archive still exists, because 7-zip returned warnings or errors:', path_output_tmp)
        
        # Display information about the created file
        print('Created:', path_output)
        print('Size:', binaryprefix(stat(path_output).st_size))
        print('Runtime:', sec2hms(time() - time_start), '\n')
        
    print('Total Runtime:', sec2hms(time() - time_start_total), '\n')

def sec2hms(s):
    '''
    Converts seconds into hours/minutes/seconds.
    :return: String in hms format.
    '''
    (h, s) = divmod(s, 3600)
    (m, s) = divmod(s, 60)
    s = round(s)
    if s is 60:
        m += 1
        if m is 60:
            h += 1
    return '{} h {} m {} s'.format(int(h), int(m), int(s))


def binaryprefix(a):
    '''
    Converts bytes into bytes with a binary prefix. E.g. 1e9 to '1 GB'
    :return: String bytes with binary prefix.
    '''
    units = ('B', 'kB', 'MB', 'GB', 'TB')
    b = floor(log(a, 1024))
    b = min(b, len(units))
    a = round(a/1024**b, 2)
    return '{} {}'.format(a, units[b])


def zip(path_input, path_output, pw=''):
    '''
    Creates a 7z container for path_input in path_output with password pw.
    :return: True, when zip operation ended without any warnings and errors, else False.
    '''
    # Path to 7-zip
    path_7z = r'C:\Program Files\7-Zip\7z.exe'
    path_7z = str(Path(path_7z))

    # Command for compression
    command = [path_7z,
               'a', # create file (a)dd
               path_output,
               path_input,
               # '-v50g', # create 50GB multivolume file
               '-mx0', # no compression
               '-p' + pw, # set password
               '-mhe' # encrypt headers
               ]
    
    # print('Running: ', subprocess.list2cmdline(command))

    # Run zip command
    sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Print live output from 7-zip
    everything_ok = False
    for line in sp.stdout.readlines():
        line = line.decode(encoding='utf-8', errors='ignore').rstrip()
        print('[7-zip Output]', line)

    return 'Everything is Ok' in line
    

if __name__ == '__main__':
    example()
