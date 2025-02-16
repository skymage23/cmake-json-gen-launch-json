#! /usr/bin/env python3

import json
#import sys
#
#sys.path("")
#
#from os_check import is_windows
#
#def create_debug_config(name, program_path, debugger="gdb"):
#    return {
#        "name": f"Debug {name}",
#        "type": "cppvsdbg" if is_windows() else "cppdbg",
#        "request": "launch",
#        "program": f"${{workspaceFolder}}/{program_path}",
#        "cwd": "${workspaceFolder}",
#        "MIMode": debugger,
#        "miDebuggerPath": f"/usr/bin/{debugger}"
#    }
#
#def create_run_config(name, program_path):
#    return {
#        "name": f"Run {name}",
#        "type": "cppvsdbg" if is_windows() else "cppdbg",
#        "request": "launch",
#        "program": f"${{workspaceFolder}}/{program_path}",
#        "cwd": "${workspaceFolder}",
#        "MIMode": "none"
#    }
#def generate_launch_json(executable_clusters):
#    configurations = []
#    
#    for cluster in executable_clusters:
#        path, name, exe_type = cluster.split(',')
#        
#        # Debug configuration for all executables
#        configurations.append(create_debug_config(name, path))
#        
#        # Run configuration only for release executables
#        if exe_type.lower() == "release":
#            configurations.append(create_run_config(name, path))
#    
#    launch_config = {
#        "version": "0.2.0",
#        "configurations": configurations
#    }
#    
#    return json.dumps(launch_config, indent=4)
#
#if __name__ == "__main__":
#    if len(sys.argv) < 2:
#        print("Usage: generate_launch_json.py <path,name,type> [<path,name,type> ...]")
#        sys.exit(1)
#    
#    launch_json = generate_launch_json(sys.argv[1:])
#    print(launch_json)