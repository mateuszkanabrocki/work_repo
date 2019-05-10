from os.path import exists
from os import remove
import sys
import os
this_module = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.join(this_module, f'sessions/{filename}.txt'))

def delete_file(filename, gothonweb_path):
    # testfile_path = f"{gothonweb_path}/sessions/{filename}.txt"
    testfile_path = os.path.join(os.path.dirname(__file__), f'sessions/{filename}.txt')
    remove(testfile_path)