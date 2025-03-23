#! /usr/bin/env python3

import argparse
import copy
import hashlib
import importlib
import json
import os
import pathlib
import sys

import validation_schemas

python_dir = pathlib.Path(__file__).parent
scripts_dir = python_dir.parent
gen_launch_json_base_dir = scripts_dir.parent
third_party_dir = (gen_launch_json_base_dir / "third_party")
sys.path.append(third_party_dir.__str__())

#I know this is clunky, but it will have to do for now.
usefulbuildsystools = importlib.import_module("python-useful-build-sys-tools")
usefulbuildsystools.initialize()

import os_utilities
from error_handling import errcode_handling


class TargetItem:
    def __init__(self, name, prog_language, bin_path, is_debug):
        self.name = name
        self.prog_language = prog_language
        self.bin_path = bin_path
        self.is_debug = is_debug

    def __str__(self):
        return f"""Name: {self.name}
Programming Language: {self.prog_language}
Binary path: {self.bin_path}
Is debug: {self.is_debug}

"""



class LanguageHandlersAndCallbacks:

    def input_validation(self, binary_path, is_debug):
        return errcode_handling.SUCCESS_ERRCODE

    def autodetect_handler(self, target_item: TargetItem, json_retval_obj):
        pass

class CplusplusLanguageHandlersAndCallbacks(LanguageHandlersAndCallbacks):
    def __init__(self):
        self.ERRCODE_NO_BINARY = errcode_handling.register_errcode(
            "cplusplus_NO_BINARY_PATH",
            "No binary path specified. For cplusplus targets, a binary path must be specificed"
        )

    
    #returns errcode,
    def input_validator(self, binary_path, is_debug):
        if binary_path is None:
            print("For cplusplus targets, a binary path must be specified.", file=sys.stderr)
            return False
        return True

    def autodetect_handler(self, target_item: TargetItem, json_retval_obj):
        json_retval_obj["program"] = target_item.bin_path

supported_prog_languages = {}
supported_prog_languages["cplusplus"] = CplusplusLanguageHandlersAndCallbacks()



def die(message: str):
    print(message, file=sys.stderr)
    exit(1)


#The end result of this function is that we have language-specific templates
#that also account for host-os-specific attributes.  Target-specific
#modifications will be conducted on a case-by-case basis by this
#function's caller.
def gen_prog_lang_templates(
     base_template,
     host_os   
):
    
    #Extract general, host os specific attributes:
    retval_template = {}
    os_specific = None
    language_specific = None
    for key in base_template:
        if key  == "os_specific":
            os_specific = base_template[key]
            continue

        if key == "language-specific":
            language_specific = base_template[key]
            continue

        retval_template[key] = base_template[key]

    if (os_specific is not None) and (host_os in os_specific):
        #Override generic attributes with os-specific settings:
        #for key in os_specific[host_os]:
            #retval_template[key] = os_specific[host_os][key]
        os_specific = None
        retval_template.update(os_specific[host_os])

    #This is where things get a bit hairy.
    temp = None
    retval_dict = {"generic": retval_template}

    if language_specific is not None:
        for key in language_specific:
            temp = copy.deepcopy(retval_template)
            #Override generic, host-os-specific attributes with generic, language-specific settings.
            for inner_key in language_specific[key]:
                if inner_key == "os_specific":
                    os_specific = language_specific[key][inner_key]
                    continue
                temp[inner_key] = language_specific[key][inner_key]

            if (os_specific is not None) and (host_os in os_specific):
                #Override generic, host-os-specific, generic language-specific settings with
                #language-specific settings that change according to the host os.
               # for inner_key in os_specific[host_os]:
               #     temp[inner_key] = os_specific[host_os][inner_key]
                temp.update(os_specific[host_os])
                os_specific = None
            retval_dict[key] = temp

    #The end result is a dict of Python objects, one representing the configurations
    #specific to each supported programming language given their being used to build and run
    #targets on the host machine in addition to a set of generic launch settings. 
    return retval_dict



#How the final configuration JSON objects are generated:
#gen_attributes -> apply os-specific rules -> apply language specific rules ->
#apply language and OS specific rules -> apply target-specific rules.
ERRCODE_JSON_VALIDATION = errcode_handling.register_errcode(
    "json_validation",
    "Unable to validate input JSON."
)
def generate_python_json_dict(
        targets,
        global_template_filepath,
        target_specific_dir
    ):

    host_os = "other"

    #These platforms have certain configuration rules that apply uniquely to them.
    if os_utilities.is_linux():
        host_os = "linux"
    elif os_utilities.is_windows():
        host_os = "windows"
    elif os_utilities.is_macos():
        host_os = "osx"

    config_arr = []
    global_template = validation_schemas.validate_json(
        global_template_filepath
    )
     
    if global_template is None:
        return ERRCODE_JSON_VALIDATION, None
    
    supported_prog_langs = validation_schemas.get_supported_programming_languages()
    target_specific_configs = None
    temp_filepath = None
    temp_json = None
    temp_entry = None
    target_prog_lang_templates = None

    #Create language templates:
    prog_language_templates = gen_prog_lang_templates(
        global_template,
        host_os
    )

    for item in targets:
        if item.prog_language in supported_prog_langs:
            temp_entry = copy.deepcopy(prog_language_templates[item.prog_language])
        else:
            temp_entry = copy.deepcopy(prog_language_templates["generic"])

        temp_entry["name"] = item.name 
        if target_specific_dir is not None:
            temp_filepath = (target_specific_dir / f"{item.name}.json")
            if temp_filepath.exists():
                temp_json = validation_schemas.validate_json(temp_filepath.__str__())
                if temp_json is None:
                    return ERRCODE_JSON_VALIDATION, None
                #collate:
                target_prog_lang_templates = gen_prog_lang_templates(
                    temp_json,
                    host_os
                )

                if item.prog_language in target_prog_lang_templates:
                    target_specific_configs = target_prog_lang_templates[item.prog_language]
                else:
                    target_specific_configs = target_prog_lang_templates["generic"]
#                for key in target_specific_configs:
#                    temp_entry[key] = target_specific_configs[key]
#
                temp_entry.update(target_specific_configs)
        
        #Need better way of setting auto-detected yet programming language specific attributes,
        #such as this.
        if item.prog_language in supported_prog_languages:
            (supported_prog_languages[item.prog_language]).autodetect_handler(item, temp_entry)

        config_arr.append(temp_entry)
    return errcode_handling.SUCCESS_ERRCODE, {"configurations": config_arr}
    

def write_launch_json_file(config_obj, proj_base_dir):
    raise NotImplementedError()

#Unrecoverable, SHA1 hash, target_list
ERRCODE_INVALID_TARGET_LIST = errcode_handling.register_errcode(
    "INVALID_TARGET_LIST",
    "Target list file does not contain a valid list of targets"
)
ERRCODE_TARGET_FILE_NOT_FOUND = errcode_handling.register_errcode(
    "TARGET_FILE_NOT_FOUND",
    "Target list file not found."
)
ERRCODE_PERMISSION_ERROR = errcode_handling.register_errcode(
    "PERMISSION_ERROR",
    "File access permission denied."
)
def get_target_list(filename: str):
    lines = None
    errcode = errcode_handling.GENERIC_ERROR_ERRCODE
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        if (len(lines) >= 2):
            return errcode_handling.SUCCESS_ERRCODE, lines[0].strip(), [line.strip() for line in lines[1:]]
        

    except FileNotFoundError:
        errcode = ERRCODE_TARGET_FILE_NOT_FOUND
    except PermissionError:
        errcode = ERRCODE_PERMISSION_ERROR
    return errcode, None, None

def get_sha1_hash(target_list):
    hasher = hashlib.sha1()
    for elem in sorted(target_list):
        hasher.update(elem.encode())
    return hasher.hexdigest()

#Fix error handling here:
#unrecoverable_error, list of targets as arrays.
#Target list record: name, programming language, binary path, is debug
ERRCODE_TOO_FEW_FIELDS = errcode_handling.register_errcode(
    "TOO_FEW_FIELDS",
    "Target item parse error: too few fields"
)

ERRCODE_TARGET_ITEM_NAME_EMPTY = errcode_handling.register_errcode(
    "TARGET_ITEM_NAME_EMPTY",
    "Target item parse error: name cannot be empty."
)

ERRCODE_TARGET_ITEM_PROG_LANG_EMPTY = errcode_handling.register_errcode(
    "TARGET_ITEM_PROG_LANG_EMPTY",
    "Target item parse error: programming language cannot be empty."
)

ERRCODE_TARGET_ITEM_IS_DEBUG_EMPTY = errcode_handling.register_errcode(
    "TARGET_ITEM_IS_DEBUG_EMPTY",
    "Target item parse error: is_debug cannot be empty."
)

#Errcode, problematic_entry, parsed_target_array
def parse_target_list(target_list):
     name = None
     programming_language = None
     binary_path = None
     is_debug_str = None
     is_debug = False
     temp_errcode = None

     split_items = None
     retval = []
     for item in target_list:
        split_items = item.split(',')
        if(len(split_items) < 4):
            return ERRCODE_TOO_FEW_FIELDS, item, None #Malformed target list entry.
        name = split_items[0].strip()
        if len(name) == 0:
            return ERRCODE_TARGET_ITEM_NAME_EMPTY, item, None #Name vannot be empty.
        programming_language = split_items[1].strip()
        if len(programming_language) == 0:
            return ERRCODE_TARGET_ITEM_PROG_LANG_EMPTY, item, None #Programming language cannot be empty.

        binary_path = split_items[2].strip() if len(split_items[2]) > 0 else None

        is_debug_str = split_items[3].strip()
        if len(is_debug_str) == 0:
            return ERRCODE_TARGET_ITEM_IS_DEBUG_EMPTY, item, None #is_debug cannot be empty.
        is_debug = split_items[3] == "true"

        if (programming_language in supported_prog_languages):
             temp_errcode = (supported_prog_languages[programming_language]).input_validation(binary_path, is_debug)
             if (temp_errcode != errcode_handling.SUCCESS_ERRCODE):
                 return temp_errcode, item, None #Failed language-specific validation

        retval.append(
            TargetItem(
                name,
                programming_language,
                binary_path,
                is_debug
            )
        )
     return errcode_handling.SUCCESS_ERRCODE, None, retval


def write_launch_json(vscode_dir_path, launch_json_obj):
    errcode = errcode_handling.SUCCESS_ERRCODE
    try:
        if not vscode_dir_path.exists():
            os.mkdir(vscode_dir_path.__str__())

        with open((vscode_dir_path/ "launch.json").__str__(), "w") as file:
            json.dump(launch_json_obj, file)
    except PermissionError:
        errcode = ERRCODE_PERMISSION_ERROR
    except Exception as e:
        errcode = errcode_handling.GENERIC_ERROR_ERRCODE

    return errcode


def main():
    global_template_filename = "global_launch_config_template.json"
    target_specific_dirname = "target_specific_launch_configs"
    parser = argparse.ArgumentParser(
        prog="gen_launch_json.py",
        description=f"""
Generates VS Codes \"launch.json\" file using \"{global_template_filename}\"
and \"{target_specific_dirname}\", both located under the project base directory."
"""
    )
    parser.add_argument(
        "project_base_directory",
        help="The base directory of the project."
    )

    parser.add_argument(
        "target_list_file",
        help="""
File path to the target list file. Typically, this file is automatically is
automatically generated when CMake is ran."""
    )

    args = parser.parse_args()
    proj_base = pathlib.Path(args.project_base_directory)
    vscode_dir = proj_base / ".vscode"
    global_template_filepath = proj_base / global_template_filename
    
    if not global_template_filepath.exists():
        return 0
    
    target_specific_dir = proj_base / "target_specific_launch_configs"
    if not target_specific_dir.exists():
        target_specific_dir = None

    filename = pathlib.Path(args.target_list_file)

    if not filename.exists():
        die(f"Target list file \"{filename.__str__()}\" does not exist")

    errcode, hash, target_list = get_target_list(filename.__str__())
    if errcode != errcode_handling.SUCCESS_ERRCODE:
        die(errcode_handling.get_message(errcode))

    calcd_hash = get_sha1_hash(target_list)
    if hash != calcd_hash:
        die("It looks like the target list file was corrupted.  It will need to be regenerated.")

    errcode, malformed_entry, parsed_targets = parse_target_list(target_list)
    if errcode != errcode_handling.SUCCESS_ERRCODE:
        print(f"Unable to parse target list. Malformed entry: {malformed_entry}", file=sys.stderr)
        die(errcode_handling.get_message(errcode))

    errcode, collated_json_dict = generate_python_json_dict(
        parsed_targets,
        global_template_filepath.__str__(),
        target_specific_dir
    )

    if errcode != errcode_handling.SUCCESS_ERRCODE:
        die(errcode_handling.get_message(errcode))

    errcode = write_launch_json(vscode_dir, collated_json_dict)
    if errcode != errcode_handling.SUCCESS_ERRCODE:
        die(errcode_handling.get_message(errcode))
    

if __name__ == "__main__":
    exit(main())