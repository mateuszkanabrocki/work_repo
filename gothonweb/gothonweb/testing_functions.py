from os.path import exists
from os import remove


def delete_file(filename, gothonweb_path):
    testfile_path = f"{gothonweb_path}/gothonweb/sessions/{filename}.txt"
    try:
        remove(testfile_path)
    except:
        raise Exception('app_test.py has hardcoded gothonweb project location path - you need to change it to run nosetests')