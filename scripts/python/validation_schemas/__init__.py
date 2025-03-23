import hashlib
import json
import jsonschema
import os
import pathlib
import referencing
import re
import sys

validation_schema_dir = pathlib.Path(__file__).parent
json_schema_dir = (validation_schema_dir / "json_schemas")
python_dir = validation_schema_dir.parent
scripts_dir = python_dir.parent
proj_base = scripts_dir.parent
third_party_dir = proj_base / "third_party"

sys.path.append(third_party_dir.__str__())
import development_shell_helpers.imports.Python3.Universal.repo_utils as repo_utils

#We have two functions that need to iterate through the JSON files
#in the schema. Why should we duplicate the looping code?
def _iterate_through_json_schema_files_and_run_func_on_each(func):
    for root, _, files in os.walk(json_schema_dir.__str__()):
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
    pre_calcd_hash = "acb617e02bdb10055b59edf7f9f83cf89ee136e6"
    calcd_hash = _get_sha1_schema_hash()
    return pre_calcd_hash == calcd_hash

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

def get_supported_programming_languages():
    retval = []
    for root, dirs, files in os.walk((json_schema_dir/ "prog_languages").__str__()):
        retval.extend([d for d in dirs])
        del dirs[:]
    return retval