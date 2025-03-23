import unittest


#stdlib:
import copy
import json
import shared_data
import subprocess
import sys


#Initialize custom import paths:
import initializer
initializer.initialize()

#custom modules
import development_shell_helpers.imports.Python3.Universal.repo_utils as repo_utils
import development_shell_helpers.imports.Python3.Specific.RepoUtils.Errors as repo_utils_errors
import os_utilities
from error_handling import errcode_handling
import validation_schemas


#Under test:
import gen_launch_json



class TestGenLaunchJson(unittest.TestCase):
    def setUp(self):
        test_help_dir = (shared_data.test_helper_dir / "test_gen_launch_json")
        global_template_path = (test_help_dir / "global_launch_config_template.json")
        if not test_help_dir.exists() or \
           not global_template_path.exists():
            raise repo_utils_errors.RepoCorruptError()
         
        self.test_helper_dir = test_help_dir
        self.global_template_path = global_template_path
        self.target_list_path = (self.test_helper_dir / "target_list.txt")

        super().setUp()

    def test_get_target_list(self):
        errcode, _, targets = gen_launch_json.get_target_list(self.target_list_path.__str__())

        print(errcode_handling.get_message(errcode))
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        self.assertTrue( "dorks" in targets[0]) 

    def test_check_hash(self):
        errcode, hash, targets = gen_launch_json.get_target_list(self.target_list_path.__str__())

        print(errcode_handling.get_message(errcode)) 
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        calcd_hash = gen_launch_json.get_sha1_hash(targets)
        self.assertEqual(calcd_hash, hash)

    def test_parse_target_list(self): 
        errcode, _, targets = gen_launch_json.get_target_list(self.target_list_path.__str__())
        print(errcode_handling.get_message(errcode))
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)

        errcode, errd_item, parsed_targets = gen_launch_json.parse_target_list(targets) 
        print(errcode_handling.get_message(errcode))
        print(errd_item)
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        self.assertIsNotNone(parsed_targets)
        self.assertEqual(len(parsed_targets), 5)




    def test_gen_prog_lang_templates(self):
        ground_truth_template = {
            "generic": {
                "args": "--this-is-fake --so-is-this -f",
                "cwd": "/home/user/workspace",
                "environment": {
                    "FAKE_ENV": "THIS IS FAKE"
                }
            },
            "cplusplus": {
                "args": "--this-is-fake --so-is-this -f",
                "cwd": "/home/user/workspace",
                "environment": {
                    "FAKE_ENV": "THIS IS FAKE"
                },
                "additionalSOLibSearchPath": None,
                "externalConsole": True,
                "logging": "exceptions",
                "visualizerFile": None,
                "showDisplayString": True,
                "stopAtEntry": False,
                "stopAtConnect": False,
                "setupCommands": [],
                "customLaunchSetupCommands": [],
                "launchCompleteCommand": "exec-run",  
                "symbolLoadInfo": {
                    "loadAll": True,
                    "exceptionList": None
                },
                "miDebuggerServerAddress": None,
                "debugServerPath": None,
                "debugServerArgs": None,
                "serverStarted": None,
                "filterStdout": False,
                "filterStderr": False,
                "serverLaunchTimeout": 100000,
                "pipeTransport": {
                    "pipeCwd": "/home/user/tmp",
                    "pipeProgram": "/usr/bin/ssh",
                    "pipeArgs": ["user@theserver.net.com.org"],
                    "debuggerPath": "/usr/bin/gdb"
                },
                "hardware_breakpoints": {
                    "require": False,
                    "limit": 10
                },
                "processId": "${command:pickProcess}",
                "request": "launch",
                "targetArchitecture": "x86-64",
                "sourceFileMap": {},
                "miDebuggerArgs": "",
            }
        }

        if os_utilities.is_linux():
            host_os = "linux"
            ground_truth_template["cplusplus"]["miDebuggerPath"] = "/usr/bin/gdb"
            ground_truth_template["cplusplus"]["miDebuggerArgs"] = None
            ground_truth_template["cplusplus"]["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_macos():
            host_os = "osx"
            ground_truth_template["cplusplus"]["MIMode"] = "lldb"
            ground_truth_template["cplusplus"]["miDebuggerPath"] = "lldb"
            ground_truth_template["cplusplus"]["miDebuggerArgs"] = None
            ground_truth_template["cplusplus"]["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_windows():
            host_os = "windows"
            ground_truth_template["cplusplus"]["symbolSearchPath"] = "C:\\Users\\user\\Document\\coding\\native\\symbols"
            ground_truth_template["cplusplus"]["requireExactSource"] = False
            ground_truth_template["cplusplus"]["MIMode"] = "gdb"
            ground_truth_template["cplusplus"]["miDebuggerPath"] = "C:\\Users\\user\\bin\\gdb"
            ground_truth_template["cplusplus"]["miDebuggerArgs"] = None
            ground_truth_template["cplusplus"]["dumpPath"] = "C:\\Users\\users\\Document\\coding\\native\\core_dumps"

        global_template = validation_schemas.validate_json(
            self.global_template_path.__str__(),
            host_os
        )

        calcd_json_dict = gen_launch_json.gen_prog_lang_templates(
            global_template,
            host_os
        );
        self.maxDiff = None
        self.assertEqual(calcd_json_dict, ground_truth_template)

    def test_generate_python_json_dict(self):
        errcode, _, targets = gen_launch_json.get_target_list(self.target_list_path.__str__())
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
    
        errcode, errd_item, parsed_targets = gen_launch_json.parse_target_list(targets) 
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        self.assertIsNotNone(parsed_targets)
        self.assertEqual(len(parsed_targets), 5)
    
        ground_truth_generic_template = {
            "args": "--this-is-fake --so-is-this -f",
            "cwd": "/home/user/workspace",
            "environment": {
                "FAKE_ENV": "THIS IS FAKE"
            }
        }
      
        ground_truth_template = copy.deepcopy(ground_truth_generic_template)
        ground_truth_template.update({ 
                "additionalSOLibSearchPath": None,
                "externalConsole": True,
                "logging": "exceptions",
                "visualizerFile": None,
                "showDisplayString": True,
                "stopAtEntry": False,
                "stopAtConnect": False,
                "setupCommands": [],
                "customLaunchSetupCommands": [],
                "launchCompleteCommand": "exec-run",  
                "symbolLoadInfo": {
                    "loadAll": True,
                    "exceptionList": None
                },
                "miDebuggerServerAddress": None,
                "debugServerPath": None,
                "debugServerArgs": None,
                "serverStarted": None,
                "filterStdout": False,
                "filterStderr": False,
                "serverLaunchTimeout": 100000,
                "pipeTransport": {
                    "pipeCwd": "/home/user/tmp",
                    "pipeProgram": "/usr/bin/ssh",
                    "pipeArgs": ["user@theserver.net.com.org"],
                    "debuggerPath": "/usr/bin/gdb"
                },
                "hardware_breakpoints": {
                    "require": False,
                    "limit": 10
                },
                "processId": "${command:pickProcess}",
                "request": "launch",
                "targetArchitecture": "x86-64",
                "sourceFileMap": {},
                "miDebuggerArgs": "",
            })
        if os_utilities.is_linux():
            host_os = "linux"
            ground_truth_template["miDebuggerPath"] = "/usr/bin/gdb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_macos():
            host_os = "osx"
            ground_truth_template["MIMode"] = "lldb"
            ground_truth_template["miDebuggerPath"] = "lldb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_windows():
            host_os = "windows"
            ground_truth_template["symbolSearchPath"] = "C:\\Users\\user\\Document\\coding\\native\\symbols"
            ground_truth_template["requireExactSource"] = False
            ground_truth_template["MIMode"] = "gdb"
            ground_truth_template["miDebuggerPath"] = "C:\\Users\\user\\bin\\gdb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["dumpPath"] = "C:\\Users\\users\\Document\\coding\\native\\core_dumps"
    
        temp = None;
        ground_truth = {"configurations":[]}


        for target in parsed_targets:
            #breakpoint()
            if target.prog_language in validation_schemas.get_supported_programming_languages():
                temp = copy.deepcopy(ground_truth_template)
            else:
                temp = copy.deepcopy(ground_truth_generic_template)

            temp["name"] = target.name
            if target.name == "dorks":
                temp["environment"] = {"BIKER": True}
            if target.prog_language == "cplusplus":
                temp["program"] = target.bin_path
            ground_truth["configurations"].append(temp)

        #for target in parsed_targets:
        #    temp = copy.deepcopy(ground_truth_template)
        #    temp["name"] = target.name
        #    if target.name == "dorks":
        #        temp["environment"] = {"BIKER": True}
        #    if target.prog_language == "cplusplus":
        #        temp["program"] = target.bin_path
        #    ground_truth["configurations"].append(temp)
        
        errcode, calcd_json = gen_launch_json.generate_python_json_dict(
            parsed_targets,
            self.global_template_path.__str__(),
            (self.test_helper_dir / "target_specific_launch_configs")
        )
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        self.assertEqual(calcd_json, ground_truth)
        
    def test_cli_call(self):
        errcode, _, targets = gen_launch_json.get_target_list(self.target_list_path.__str__())
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
    
        errcode, errd_item, parsed_targets = gen_launch_json.parse_target_list(targets) 
        self.assertEqual(errcode, errcode_handling.SUCCESS_ERRCODE)
        self.assertIsNotNone(parsed_targets)
        self.assertEqual(len(parsed_targets), 5)

        ground_truth_generic_template = {
            "args": "--this-is-fake --so-is-this -f",
            "cwd": "/home/user/workspace",
            "environment": {
                "FAKE_ENV": "THIS IS FAKE"
            }
        }
      
        ground_truth_template = copy.deepcopy(ground_truth_generic_template)
        ground_truth_template.update({ 
                "additionalSOLibSearchPath": None,
                "externalConsole": True,
                "logging": "exceptions",
                "visualizerFile": None,
                "showDisplayString": True,
                "stopAtEntry": False,
                "stopAtConnect": False,
                "setupCommands": [],
                "customLaunchSetupCommands": [],
                "launchCompleteCommand": "exec-run",  
                "symbolLoadInfo": {
                    "loadAll": True,
                    "exceptionList": None
                },
                "miDebuggerServerAddress": None,
                "debugServerPath": None,
                "debugServerArgs": None,
                "serverStarted": None,
                "filterStdout": False,
                "filterStderr": False,
                "serverLaunchTimeout": 100000,
                "pipeTransport": {
                    "pipeCwd": "/home/user/tmp",
                    "pipeProgram": "/usr/bin/ssh",
                    "pipeArgs": ["user@theserver.net.com.org"],
                    "debuggerPath": "/usr/bin/gdb"
                },
                "hardware_breakpoints": {
                    "require": False,
                    "limit": 10
                },
                "processId": "${command:pickProcess}",
                "request": "launch",
                "targetArchitecture": "x86-64",
                "sourceFileMap": {},
                "miDebuggerArgs": "",
            })
        
        if os_utilities.is_linux():
            ground_truth_template["miDebuggerPath"] = "/usr/bin/gdb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_macos():
            ground_truth_template["MIMode"] = "lldb"
            ground_truth_template["miDebuggerPath"] = "lldb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["coreDumpPath"] = "/home/user/workspace"
        elif os_utilities.is_windows():
            ground_truth_template["symbolSearchPath"] = "C:\\Users\\user\\Document\\coding\\native\\symbols"
            ground_truth_template["requireExactSource"] = False
            ground_truth_template["MIMode"] = "gdb"
            ground_truth_template["miDebuggerPath"] = "C:\\Users\\user\\bin\\gdb"
            ground_truth_template["miDebuggerArgs"] = None
            ground_truth_template["dumpPath"] = "C:\\Users\\users\\Document\\coding\\native\\core_dumps"
    
        temp = None;
        ground_truth = {"configurations":[]}
        for target in parsed_targets:
            if target.prog_language in validation_schemas.get_supported_programming_languages():
                temp = copy.deepcopy(ground_truth_template)
            else:
                temp = copy.deepcopy(ground_truth_generic_template)
            temp["name"] = target.name
            if target.name == "dorks":
                temp["environment"] = {"BIKER": True}
            if target.prog_language == "cplusplus":
                temp["program"] = target.bin_path
            ground_truth["configurations"].append(temp)

        with open("ground_truth.json", "w") as file:
            json.dump(ground_truth, file)
        
    
        process_ret = subprocess.run(
            [
                sys.executable,
                (shared_data.main_python_path / "gen_launch_json.py").__str__(),
                (self.test_helper_dir).__str__(),
                (self.test_helper_dir / "target_list.txt").__str__()
            ],
            stdout = sys.stdout,
            stderr = sys.stderr
        )
        self.assertEqual(process_ret.returncode, 0)
    
    
        vscode_path = (self.test_helper_dir / ".vscode")
        self.assertTrue(vscode_path.exists())
    
        with open((vscode_path / "launch.json").__str__(), 'r') as file:
            calcd_json = json.load(file)
        
        self.maxDiff = None
        self.assertEqual(calcd_json, ground_truth)
