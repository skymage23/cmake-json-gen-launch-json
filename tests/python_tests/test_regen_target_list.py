import importlib
import os
import subprocess
import unittest

import errors

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

class TestRegenTargetList(unittest.TestCase):

    def load_hash_and_target_list_from_file(filename):
        target_list = None
        with open(filename, 'r') as file:
            target_list = file.readlines()
        return target_list[0].strip(), target_list[1:]
    
    def get_sample_file_name():
        filename = (sha1_test_helper_dir / "sample_file_name.txt")
        retval = None
        with open(filename, 'r') as file:
            retval = file.readline().strip()
        
        retval = (sha1_test_helper_dir / retval).__str__()
        return retval

    def generate_sample_target_list_file():
        generator_filepath = None
        shell = os_utilities.get_os_helper().get_shell() 
        
        if os_utilities.is_windows():
            generator_filepath = (sha1_test_helper_dir / "gen_sample_output_file.ps1").__str__()
        else:
            generator_filepath = (sha1_test_helper_dir / "gen_sample_output_file.sh").__str__()
      
        process_ret = subprocess.run(
            [shell, generator_filepath],
            capture_output=True
        )
        return (process_ret.returncode == 0)

    #Hello:
    def setUp(self) -> None:
        if not TestRegenTargetList.generate_sample_target_list_file():
            raise errors.SampleFileGenerationError()

        filename = (sha1_test_helper_dir / "raw_sample_target_list.txt").__str__()
        target_list = None
        with open(filename, 'r') as file:
            target_list = file.readlines()
    
        for i in range(0,len(target_list)):
            target_list[i] = target_list[i].lower()
            
        target_list.sort()
        
        self.sample_file_name = TestRegenTargetList.get_sample_file_name()
        self.app_singleton = sha1hash.ApplicationSingleton(None, target_list) 
        return super().setUp()
    

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
        with open(target_filepath, 'r') as file:
            gen_file_lines = file.readlines()

        file_hash = gen_file_lines[0].strip()
        gen_target_list = gen_file_lines[1:]

        hash, sample_file_lines = TestRegenTargetList.load_hash_and_target_list_from_file(
            self.sample_file_name
        )
        
        gen_target_list_len = len(gen_target_list)
        self.assertEqual(file_hash, hash)
        self.assertEqual(gen_target_list_len, len(sample_file_lines))

        for i in range(0, gen_target_list_len):
            self.assertEqual(gen_target_list[i], sample_file_lines[i])

       # os.remove(target_filepath)

    def test_get_stored_hash(self):
        py_digest = sha1hash.hash_target_list(self.app_singleton)
        target_filepath = (sha1_test_helper_dir / "generated_target_list_file.txt").__str__()
        self.app_singleton.output_file = target_filepath
        sha1hash.write_target_list_file(py_digest, self.app_singleton)

        hash = sha1hash.get_stored_hash(self.app_singleton)

        self.assertEqual(hash, py_digest)

    def test_hash_and_compare(self):
        py_digest = sha1hash.hash_target_list(self.app_singleton)
        target_filepath = (sha1_test_helper_dir / "generated_target_list_file.txt").__str__()
        self.app_singleton.output_file = target_filepath
        sha1hash.write_target_list_file(py_digest, self.app_singleton)

        self.assertTrue((sha1hash.hash_and_compare(self.app_singleton))[0])
