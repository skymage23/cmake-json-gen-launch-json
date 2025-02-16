include_guard(GLOBAL)
include("${CMAKE_CURRENT_LIST_DIR}/python-integration-common.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/os_host_setup.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../third_party/cmake-build-sys-utilities/scripts/build_sys_opts.cmake")

    
set(PROJECT_BASE "${CMAKE_SOURCE_DIR}") #This SHOULD be set to the current project base

#Here is our strategy:
function(write_targets_list_file)
    get_targets_list_under_dir()
    set(cmd_list ${cmd_list_template})
    #This script hashes its input and then checks the hash against
    #a set file under the ${CMAKE_BUILD_DIR} directory.
    list(APPEND cmd_list "${PYTHON_SCRIPT_DIR_PATH}/sha1-hash-args.py")
    list(APPEND cmd_list ${OUTPUT_TARGET_TEMP})
    execute_process(
        COMMAND ${cmd_list}
        WORKING_DIRECTORY "${PYTHON_SCRIPT_DIR_PATH}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()