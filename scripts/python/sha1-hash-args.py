import argparse
import hashlib
import sys

"""
This script takes in a list of CMake targets,
hashes them, and then, if a file of the correct name
exists in the specified target directory, reads
the hash on the first line of that file and compares
it to the current hash. If the two hashes match,
nothing happens. Else, or if the file does not exist,
the file is created, if needed, and the hash is written
to it, followed by the list of targets with 1 target per line.
"""
#We can keep it simple and have the first argument always
#be the target output file.

class ApplicationSingleton:
    def __init__(self, output_file, target_list):
        self.sys_encoding = sys.getdefaultencoding()
        self.output_file = output_file
        self.target_list = target_list

def print_err(message):
    print(message, file=sys.stderr)

def die(message):
    print_err(message)
    exit(1)

def parse_args():
    output_file = None
    target_list = []
    argv = sys.argv[1:]
    arg_len = len(argv)
    if arg_len < 2:
        die("Too few arguments.")
    output_file = argv[0]
    
    for elem in argv[1:]:
        target_list.append(elem)
    
    target_list.sort()

    return ApplicationSingleton(output_file, target_list)
    
def hash_target_list(app_singleton):
    encoder = lambda text: text.encode(app_singleton.sys_encoding)

    hasher = hashlib.sha1()
    for elem in app_singleton.target_list:
        hasher.update(encoder(elem))

    return hasher.hexdigest()

def get_stored_hash(app_singleton):
    #def_encoding = app_singleton.sys_encoding
    hash = None
    with open(app_singleton.output_file, "r") as file:
        hash = file.readline()
    hash = hash.strip()
    return hash

#0 = hashes are equal
#1 = hashes are not equal.
def hash_and_compare(app_singleton):
    calculated_hash = hash_target_list(app_singleton)
    stored_hash = get_stored_hash(app_singleton)
    
    if calculated_hash == stored_hash:
        return True, None
    else:
        return False, calculated_hash


def write_target_list_file(hash, app_singleton):
    list_to_write = ["{}\n".format(hash)] + app_singleton.target_list
    with open(app_singleton.output_file, "w") as file:
        file.writelines(list_to_write)
    
#How do we cleanly inform the user that they do not
#have permission to write to a given directory?
def main():
    app_singleton = parse_args()

    calculated_hash = hash_target_list(app_singleton)
    stored_hash = get_stored_hash(app_singleton)
    
    if calculated_hash != stored_hash:
        write_target_list_file(calculated_hash, app_singleton)

    return 0
if __name__ == "__main__":
    exit(main())