from zipfile import ZipFile
import os
from os.path import join as p_join
from os import listdir
from os import walk

z = ZipFile('asdf.zip', 'w')

for root, dirs, files in walk('Utilities'):
    for f in files:
        z.write(p_join(root, f))
        print(p_join(root, f))
        