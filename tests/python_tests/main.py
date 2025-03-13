#!/usr/bin/env python3
import unittest

#If you import the TestCase class into the current
#module directly, it's picked up by the "unittest"
#module.
from test_regen_target_list import TestRegenTargetList
from test_json_schema import TestJsonSchema

if __name__ == "__main__":
    unittest.main()