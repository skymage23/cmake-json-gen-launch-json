include_guard(GLOBAL)
include("${CMAKE_CURRENT_LIST_DIR}/python-integration-common.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/os_host_setup.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../third_party/cmake-build-sys-utilities/scripts/build_sys_opts.cmake")

    
set(PROJECT_BASE "${CMAKE_SOURCE_DIR}") #This SHOULD be set to the current project base

#This function will only regenerate the target list file
#if the list of targets has changed.
function(gen_target_list_file)
    if(${ARGC} LESS 1)
        message(FATAL_ERROR "\"gen_target_list_file\": Too few arguments.")
    endif()
    
    if(${ARGC} GREATER 2)
        message(FATAL_ERROR "\"gen_target_list_file\": Too many arguments.")
    endif()
    
    set(oneValueArgs "OUTPUT_FILE")
    cmake_parse_arguments(gen_target_list_file "" ${oneValueArgs} "" ${ARGN})
    
    if(NOT gen_target_list_file_OUTPUT_FILE)
        message(FATAL_ERROR "OUTPUT_FILE was not specified.")
    endif()

    get_targets_list_under_dir()
    set(cmd_list ${python_cmd_list_template})
    #This script hashes its input and then checks the hash against
    #a set file under the ${CMAKE_BUILD_DIR} directory.
    list(APPEND cmd_list "${PYTHON_SCRIPT_DIR_PATH}/sha1-hash-args.py")
    list(APPEND cmd_list "${gen_target_list_file_OUTPUT_DIR}")
    list(APPEND cmd_list ${OUTPUT_TARGET_TEMP})
    execute_process(
        COMMAND ${cmd_list}
        WORKING_DIRECTORY "${PYTHON_SCRIPT_DIR_PATH}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()


set(CMAKE_SCRATCHPAD_DIR "${CMAKE_BINARY_DIR}/CMakeFiles/CMakeScratch")
set(GEN_LAUNCH_JSON_OUTPUT_FILE "${CMAKE_SCRATCHPAD_DIR}/target_list.txt")
gen_target_list_file("${GEN_LAUNCH_JSON_OUTPUT_FILE}")
add_custom_target(write_target_list_file
    COMMAND ${python_cmd_list_template}
    BYPRODUCTS "${GEN_LAUNCH_JSON_OUTPUT_FILE}"
)