import importlib
import sys
import shared_data

sys.path.append(shared_data.third_party_dir.__str__())
usefulbuildsystools = importlib.import_module("python-useful-build-sys-tools")

def initialize():
    sys.path.append(
        shared_data.main_python_path.__str__()
    )
    usefulbuildsystools.initialize() 