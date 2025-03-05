include_guard(GLOBAL)
include("${CMAKE_CURRENT_LIST_DIR}/python-integration-common.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/target_list_opts.cmake")

set(cmd_list "")
list(APPEND cmd_list "${python_cmd_list_template}")
list(APPEND cmd_list "${PYTHON_SCRIPT_DIR_PATH}/gen_launch_json.py")
list(APPEND cmd_list "${GEN_LAUNCH_JSON_OUTPUT_FILE}")

add_custom_target(gen_launch_json
    COMMAND ${cmd_list}
    BYPRODUCTS "${GEN_LAUNCH_JSON_OUTPUT_FILE}"
    MAIN_DEPENDENCY write_target_list_file
)