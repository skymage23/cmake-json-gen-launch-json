include("${CMAKE_CURRENT_LIST_DIR}/third_party/cmake-script-test-framework/cmake-test.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../scripts/target_list_opts.cmake")


macro(setup)
    set(SCRATCHPAD_DIR "${CMAKE_CURRENT_LIST_DIR}/test_helpers/scratchpad")
    if(EXISTS "${SCRATCHPAD_DIR}")
        file(REMOVE_RECURSE "${SCRATCHPAD_DIR}")
    endif()
    file(MAKE_DIRECTORY "${SCRATCHPAD_DIR}")
    file(MAKE_DIRECTORY "${SCRATCHPAD_DIR}/build")

endmacro()
add_setup_macro(MACRO_NAME setup)

macro(teardown)
    file(REMOVE_RECURSE "${SCRATCHPAD_DIR}")
    unset(SCRATCHPAD_DIR)
endmacro()
add_teardown_macro(MACRO_NAME teardown)

macro(test_gen_target_list_file)
    execute_process(
        COMMAND ${CMAKE_COMMAND} 
                -B "${SCRATCHPAD_DIR}/build" 
               "${CMAKE_CURRENT_LIST_DIR}/test_helpers/test_target_list_opts" 
               -D "OUTPUT_FILE_PATH='${SCRATCHPAD_DIR}/build/CMakeFiles/CMakeScratch/target_list.txt'"
        WORKING_DIRECTORY "${SCRATCHPAD_DIR}/build"
        RESULT_VARIABLE RESULT
        OUTPUT_VARIABLE OUTPUT
        ERROR_VARIABLE ERROR
    )
    if(NOT RESULT EQUAL 0)
        message(FATAL_ERROR "Failed to generate target list file
OUTPUT: ${OUTPUT}
ERROR: ${ERROR}
        ")
    endif()

   file(READ "${SCRATCHPAD_DIR}/build/CMakeFiles/CMakeScratch/target_list.txt" TARGET_LIST_FILE_CONTENTS)
   file(READ "${CMAKE_CURRENT_LIST_DIR}/test_helpers/test_target_list_opts/expected_target_list.txt" EXPECTED_TARGET_LIST_FILE_CONTENTS)
   if(NOT "${TARGET_LIST_FILE_CONTENTS}" STREQUAL "${EXPECTED_TARGET_LIST_FILE_CONTENTS}")
       message(FATAL_ERROR "Target list file contents do not match expected contents"
        "OUTPUT: ${OUTPUT}"
        "ERROR: ${ERROR}"
       )
   endif()
endmacro()
add_test_macro(MACRO_NAME test_gen_target_list_file TEST_GROUP "target_list_opts")

