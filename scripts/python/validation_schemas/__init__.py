import hashlib
import json
import jsonschema
import os
import pathlib
import referencing
import re
import sys

validation_schema_dirs = pathlib.Path(__file__).parent
python_dir = validation_schema_dirs.parent
scripts_dir = python_dir.parent
proj_base = scripts_dir.parent
third_party_dir = proj_base / "third_party"

sys.path.append(third_party_dir.__str__())
import development_shell_helpers.imports.Python3.Universal.repo_utils as repo_utils

#We have two functions that need to iterate through the JSON files
#in the schema. Why should we duplicate the looping code?
def _iterate_through_json_schema_files_and_run_func_on_each(func):
    schema_dir = pathlib.Path(__file__).parent / "json_schemas"
    #dir_temp = None
    #check_stack = []
    #child_dirs = None

    #check_stack.append(schema_dir)
    #regex = re.compile("\\.json$")

    #load the first
    #while not len(check_stack) <= 0:
    #    dir_temp = check_stack.pop()
    #    for item in dir_temp.iterdir():
    #        if(
    #            (not item.is_dir()) and
    #            (not regex.search(item.suffix) is None)
    #        ):
    #            func(item)    #run_lambda here:
    #        elif (item.is_dir()):
    #            if child_dirs is None:
    #                child_dirs = []
    #            child_dirs.append(item)
    for root, _, files in os.walk(schema_dir.__str__()):
        for file in sorted(files):
            if file.endswith(".json"):
                full_file_path = os.path.join(root, file)
                func(file, full_file_path)

#letting functions mutate outer scope can lead
#to tricky bugs.  Use sparingly. Here,
#it works because this function is simple
#and not intended to be used outside the module.
def _get_sha1_schema_hash():
    datablob = []
    def calc_hash(filename: str, filepath: str):
        nonlocal datablob

        datablob.append(filename)
        with open(filepath, 'r', encoding = "utf-8") as file:
            datablob.extend(file.readlines())

    _iterate_through_json_schema_files_and_run_func_on_each(calc_hash)
    
    hash_object = hashlib.sha1("".join(datablob).encode("utf-8"))
    return hash_object.hexdigest()


def _compare_schema_hash():
    #pre_calcd_hash = "145ee7d94a51177c91aaa9ead22311e4bc478c07"
    #calcd_hash = _get_sha1_schema_hash()
    #return pre_calcd_hash == calcd_hash
    return True #temp

#def _get_loaded_registry_and_main_schema():
#    schema_dir = pathlib.Path(__file__).parent / "json_schemas"
#    json_temp = None
#
#    dir_temp = None
#    check_stack = []
#    child_dirs = None
#    registry = referencing.Registry()
#    resource = None
#
#    check_stack.append(schema_dir)
#    regex = re.compile("\\.json$")
#
#    #load the first
#    while not len(check_stack) <= 0:
#        dir_temp = check_stack.pop()
#        for item in dir_temp.iterdir():
#            if(
#                (not item.is_dir()) and
#                (not regex.search(item.suffix) is None)
#            ):
#                print("Loading \"{}\"\n".format(item))
#                with open((schema_dir / item), "r") as file: 
#                    json_temp = json.load(file)
#                resource = referencing.Resource.from_contents(json_temp)
#                registry = resource @ registry
#            else:
#                if child_dirs is None:
#                    child_dirs = []
#                child_dirs.append(item)
#        #if child_dirs is not None:
#        #   for item in child_dirs:
#        #        check_stack.append(item)
#    return registry

def _get_loaded_registry_and_main_schema():
    registry = referencing.Registry()
    main_schema = None

    def load_schema(filename:str, schema_filepath: str):
        nonlocal registry
        nonlocal main_schema
        json_temp = None

        with open(schema_filepath, 'r') as file:
            json_temp = json.load(file)
        
        if filename == "schema_main.json":
            main_schema = json_temp

        resource = referencing.Resource.from_contents(json_temp)
        registry = resource @ registry

    _iterate_through_json_schema_files_and_run_func_on_each(load_schema)
    return registry, main_schema


#Validates the JSON.
def validate_json(filename, err_writer=lambda msg:print( msg, file=sys.stderr)):
    retval = None
    registry = None
    main_schema = None
    json_temp = None

    try:
        if not _compare_schema_hash():
            repo_utils.Write_RepoCorruptMessage()
            return None
        
        registry, main_schema = _get_loaded_registry_and_main_schema()

        with open(filename, "r") as file:
            json_temp = json.load(file) 
        jsonschema.validate(json_temp, schema=main_schema, registry=registry)
        retval = json_temp
    except Exception as err:
        err_writer(err.__str__())
        retval = None
    return retval