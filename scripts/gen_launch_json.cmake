include_guard(GLOBAL)
set(PROJECT_BASE "${CMAKE_SOURCE_DIR}") #This SHOULD be set to the current project base
include(${CMAKE_CURRENT_LIST_DIR}/../third_party/cmake-build-sys-utilities/scripts/build_sys_opts.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/os_host_setup.cmake)
#What do we need?
#We need the target name and the path to the binary.
#We also need to differentiate between test and release binaries.
#For test binaries, we need to make sure we accurately set the debugger.

#function(get_target_binary_path TARGET)

#Need to do a Windows check.
#set()

#endfunction()
set(ECHO_OUTPUT)
echo_parameter_using_shell("Hello, world")
message(STATUS "${ECHO_OUTPUT}")
#function(get_target_arguments)
#    set(TARGETS "")
#    set(TARGET_PATHS "")
#    set(TARGET_TYPES "")
#
#    get_targets_list_under_dir(${PROJECT_BASE})
#    set(TARGETS "${OUTPUT_TARGET_TEMP}")
#
#    foreach(TARGET in "${TARGETS}")
#       get_target_property()
#    endforeach()
#endfunction()

#function(gen_launch_json_script)
    #Hello:
#endfunction(gen_launch_json_script)
