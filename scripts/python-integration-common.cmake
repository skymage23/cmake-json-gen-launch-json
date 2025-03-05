include_guard(GLOBAL)
find_package(python3)
set(PYTHON_SCRIPT_DIR_PATH "${CMAKE_CURRENT_LIST_DIR}/python")
set(PYTHON_SCRIPT_WORKING_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

set(cmd_list_template "")
list(APPEND python_cmd_list_template "${Python3_EXECUTABLE}")
