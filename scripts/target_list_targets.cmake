include_guard(GLOBAL)
include("${CMAKE_CURRENT_LIST_DIR}/target_list_opts.cmake")

set(CMAKE_SCRATCHPAD_DIR "${CMAKE_BINARY_DIR}/CMakeFiles/CMakeScratch")
set(GEN_LAUNCH_JSON_OUTPUT_FILE "${CMAKE_SCRATCHPAD_DIR}/target_list.txt")
gen_target_list_file("${GEN_LAUNCH_JSON_OUTPUT_FILE}")

add_custom_target(write_target_list_file
    COMMAND ${python_cmd_list_template}
    BYPRODUCTS "${GEN_LAUNCH_JSON_OUTPUT_FILE}"
)