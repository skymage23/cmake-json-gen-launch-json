import unittest

import importlib
import json
import pathlib

import initializer
initializer.initialize() #Initi

validation_schema = importlib.import_module("validation_schemas")

class TestJsonSchema(unittest.TestCase): 

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
    def setUp(self):
        self.json_dir = pathlib.Path(__file__).parent.parent / "json_schema_tests"
        super().setUp()

   #Tests that the JSON schema itself is correct enough to be properly parsed.
    def test_json_schema_parse(self):
        filename = self.json_dir / "global_template.json"
        file_json = validation_schema.validate_json(filename.__str__())
        self.assertIsNotNone(file_json)

    #This test is the same as the one above in code, but
    #it serves a different purpose. This test
    #is to ensure the JSON schema is correct to a degree.
    #The previous test was to ensure the JSON schema JSON
    #files can be successfully parsed at all.
    def test_json_global_template_parse(self):
        filename = self.json_dir / "global_template.json"
        file_json = validation_schema.validate_json(filename.__str__())
        self.assertIsNotNone(file_json)
    
    def test_json_target_specific_template_parse(self):
        filename = self.json_dir / "target_specific.json"
        file_json = validation_schema.validate_json(filename.__str__())
        self.assertIsNotNone(file_json)