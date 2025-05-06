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
        self.encoding = sys.getdefaultencoding()
        self.output_file = output_file
        self.target_list = target_list

    def __str__(self):
        return "ApplicationSingleton(output_file={}, target_list={})".format(self.output_file, self.target_list)

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
    encoder = lambda text: text.encode(encoding = app_singleton.encoding)

    hasher = hashlib.sha1()
    new_list = []
    for elem in app_singleton.target_list:
        new_list.append(elem.lower().strip())

    for elem in sorted(new_list):
        hasher.update(encoder(elem))

    return hasher.hexdigest()

def get_stored_hash(app_singleton):
    #def_encoding = app_singleton.encoding
    hash = None
    unrecoverable_error = False
    try:
        with open(app_singleton.output_file, "r", encoding=app_singleton.encoding) as file:
            hash = file.readline()
        hash = hash.strip()

    except FileNotFoundError:
        hash = None
    except PermissionError:
        unrecoverable_error = True
        print("Unable to open target list file. Permission denied.", file=sys.stderr)

    return unrecoverable_error, hash


#While we clean out newlines for hash calculation,
#they are still needed when writing to the file.
#Hence, if there are no newlines in the input,
#we add them.
def write_target_list_file(hash, app_singleton):
    temp = None
    list_to_write = ["{}\n".format(hash)]
    for i in range(0, len(app_singleton.target_list)):
        temp = app_singleton.target_list[i]
        list_to_write.append("{}\n".format(temp) if (not '\n' in temp) else temp)

    with open(app_singleton.output_file, "w", encoding=app_singleton.encoding) as file:
        file.writelines(list_to_write)
    
#How do we cleanly inform the user that they do not
#have permission to write to a given directory?
def sanity_check_target_list(target_list):
    if not target_list:
        print_err("Sanity check failed: Target list is empty.")
        exit(1)
    for entry in target_list:
        if entry.count(",") != 3:
            print_err(f"Sanity check failed: Malformed entry: {entry}")
            exit(1)
    if len(set(target_list)) != len(target_list):
        print_err("Sanity check failed: Duplicate entries found.")
        exit(1)

def main():
    app_singleton = parse_args()
    sanity_check_target_list(app_singleton.target_list)
    unrecoverable_error = False
    calculated_hash = hash_target_list(app_singleton)
    unrecoverable_error, stored_hash = get_stored_hash(app_singleton)

    if(unrecoverable_error):
        print("" ,file=sys.stderr)    
    
    if (stored_hash is None) or (calculated_hash != stored_hash):
        write_target_list_file(calculated_hash, app_singleton)

    return 0
if __name__ == "__main__":
    exit(main())