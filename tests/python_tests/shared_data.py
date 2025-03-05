import pathlib
parent_dir = (pathlib.Path(__file__)).parent
test_helper_dir = parent_dir / "test_helpers"
sha1_test_helper_dir = (test_helper_dir / "test_sha1_hash_args")
project_base = (parent_dir.parent.parent)
tests_dir = (project_base / "tests")
third_party_dir = (tests_dir / "third_party")
main_python_path = (project_base / "scripts" / "python")