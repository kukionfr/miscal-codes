import filecmp
from os.path import join, abspath
from shutil import move
from time import sleep


def migrationcheck(dir1, dir2):
    # move left only files to new location 
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if len(dirs_cmp.left_only)>0:
        for L_fileordir in dirs_cmp.left_only:
            move(join(dir1,L_fileordir),join(dir2,L_fileordir)) 
            print('moved',join(dir1,L_fileordir),'to',join(dir2,L_fileordir))
    # go into subdirectories and move left only fiels to new location
    for common_dir in dirs_cmp.common_dirs:
        subdir1 = join(dir1, common_dir)
        subdir2 = join(dir2, common_dir)
        migrationcheck(subdir1, subdir2)

dir1 = abspath('//serverdw/MOVED Adrian Johnston')
dir2 = abspath('//motherserverdw/Lab Members/Adrian')
migrationcheck(dir1, dir2)
