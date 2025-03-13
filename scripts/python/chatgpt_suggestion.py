#!/usr/bin/env python3
import hashlib
import os

schemas_dir = "./validation_schemas/json_schemas"  # Update with your actual path

hash_input = []
for root, _, files in os.walk(schemas_dir):
    for file in sorted(files):  # Sorting ensures consistency
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            hash_input.append(file)  # Include filename
            with open(file_path, "r", encoding="utf-8") as f:
                hash_input.extend(f.readlines())  # Include file contents

glob = "".join(hash_input).encode("utf-8")
hash_object = hashlib.sha1(glob)
print("Calculated SHA-1 Hash:", hash_object.hexdigest())
