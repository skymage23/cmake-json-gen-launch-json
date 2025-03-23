import unittest

import importlib
import subprocess
import sys

import local_errors

#Initialize this testing library.
import initializer
initializer.initialize()

import shared_data

#Add modules to put under test
sha1hash = importlib.import_module("sha1-hash-args")

#Add utilities
os_utilities = importlib.import_module("os_utilities")

#Module constants:
sha1_test_helper_dir = (shared_data.test_helper_dir / "test_sha1_hash_args")

#
# Testing using SHA1 can be a bit tricky as even a minor change in its
# input changes the hash. To ensure homogeneity across platforms,
# there are some ground rules that must be followed when writing
# or adjusting this test software or any sample file generation scripts. 
# Here are the rules:
# 1. All targets must be converted to lowercase.
# 2. All whitespace must be removed.
# 3. The list must be sorted alphanumerically.
# 4. The input files are encoded in UTF-8 with no BOM.
#    The targets must remain encoded the same way during
#    hashing, and all output files of generation scripts
#    must also be encoded the same way.
# 6. The Python scripts do not account for newlines and carriage returns
#    when hashing the target list. Sample file generation scripts
#    must do the same.
#

class TestRegenTargetList(unittest.TestCase):

    def load_hash_and_target_list_from_file(filename):
        target_list = None
        with open(filename, 'r', encoding="utf-8") as file:
            target_list = file.readlines()
        for i in range(0,len(target_list)):
            target_list[i] = target_list[i].strip()
        return target_list[0], target_list[1:]
    
    def get_sample_file_name():
        filename = (sha1_test_helper_dir / "sample_file_name.txt")
        retval = None
        with open(filename, 'r', encoding="utf-8") as file:
            retval = file.readline().strip()
        
        retval = (sha1_test_helper_dir / retval).__str__()
        return retval

    def generate_sample_target_list_file():
        generator_filepath = None
        shell = os_utilities.get_os_helper().get_shell() 
        #shell = "pwsh.exe"
        
        if os_utilities.is_windows():
            generator_filepath = (sha1_test_helper_dir / "gen_sample_output_file.ps1").__str__()
        else:
            generator_filepath = (sha1_test_helper_dir / "gen_sample_output_file.sh").__str__()
      
        process_ret = subprocess.run(
            [shell, generator_filepath],
            capture_output=False,
            cwd=sha1_test_helper_dir.__str__(),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        return (process_ret.returncode == 0)

    def setUp(self):
        if not TestRegenTargetList.generate_sample_target_list_file():
            raise local_errors.SampleFileGenerationError()

        filename = (sha1_test_helper_dir / "raw_sample_target_list.txt").__str__()
        target_list = None
        with open(filename, 'r', encoding="utf-8") as file:
            target_list = file.readlines()
    
        for i in range(0,len(target_list)):
            target_list[i] = target_list[i].lower().strip()
            
        target_list.sort()
        self.initialized = True            
        self.sample_file_name = TestRegenTargetList.get_sample_file_name()
        self.app_singleton = sha1hash.ApplicationSingleton(None, target_list) 
        super().setUp()

    def test_sha1_hashing(self):
        #Hello:
        py_digest = sha1hash.hash_target_list(self.app_singleton)
        hash, _ = TestRegenTargetList.load_hash_and_target_list_from_file(
            self.sample_file_name
        )
        self.assertEqual(py_digest, hash)

    def test_target_file_generation(self):
        py_digest = sha1hash.hash_target_list(self.app_singleton)
        target_filepath = (sha1_test_helper_dir / "generated_target_list_file.txt").__str__()
        self.app_singleton.output_file = target_filepath
        sha1hash.write_target_list_file(py_digest, self.app_singleton)

        gen_file_lines = None
        with open(target_filepath, 'r', encoding="utf-8") as file:
            gen_file_lines = file.readlines()


        file_hash = gen_file_lines[0].strip()
        gen_target_list = [item.strip() for item in gen_file_lines[1:]]

        hash, sample_file_lines = TestRegenTargetList.load_hash_and_target_list_from_file(
            self.sample_file_name
        )
 
        gen_target_list_len = len(gen_target_list)
        self.assertEqual(hash, file_hash)
        self.assertEqual(gen_target_list_len, len(sample_file_lines))

        for i in range(0, gen_target_list_len):
            self.assertEqual(gen_target_list[i], sample_file_lines[i])

       # os.remove(target_filepath)

    def test_get_stored_hash(self):
        calcd_hash = sha1hash.hash_target_list(self.app_singleton)
        target_filepath = (sha1_test_helper_dir / "generated_target_list_file.txt").__str__()
        self.app_singleton.output_file = target_filepath
        sha1hash.write_target_list_file(calcd_hash, self.app_singleton)

        unrecoverable_error, written_hash = sha1hash.get_stored_hash(self.app_singleton)

        self.assertFalse(unrecoverable_error)
        self.assertEqual(calcd_hash, written_hash)


    def test_run_from_cli(self):
        target_filepath = (sha1_test_helper_dir / "generated_target_list_file.txt").__str__()
        hash, sample_file_lines = TestRegenTargetList.load_hash_and_target_list_from_file(
            self.sample_file_name
        )

        process_ret = subprocess.run(
            [
                sys.executable, 
                (shared_data.main_python_path / "sha1-hash-args.py").__str__(),
                "generated_target_list_file.txt"
            ] + sample_file_lines,
            capture_output=False,
            cwd=sha1_test_helper_dir.__str__(),
            stdout=sys.stdout,
            stderr=sys.stderr
        )

        with open(target_filepath, 'r', encoding="utf-8") as file:
            gen_file_lines = file.readlines()

        self.assertEqual(process_ret.returncode, 0)
        
        file_hash = gen_file_lines[0].strip()
        self.assertEqual(file_hash, hash)


    def test_run_cli_too_few_args(self):
        process_ret = subprocess.run(
            [
                sys.executable, 
                (shared_data.main_python_path / "sha1-hash-args.py").__str__()
            ],
            capture_output=True,
            cwd=sha1_test_helper_dir.__str__(),
        )

        self.assertEqual(process_ret.returncode, 1)
        self.assertEqual(process_ret.stderr.decode(), f"Too few arguments.\n")
