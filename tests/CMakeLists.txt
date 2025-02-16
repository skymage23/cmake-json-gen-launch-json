cmake_minimum_required(VERSION 3.31)
project(gen_launch_json_script_test)
include(../scripts/gen_launch_json.cmake)

#*************************************************
#                 Test Setup Header:             *
#*************************************************
find_program(VALGRIND_BINARY
    NAMES valgrind
    HINTS "/usr/bin" "/usr/local/bin" 
)

if(${VALGRIND_BINARY} STREQUAL "VALGRIND_BINARY-NOTFOUND")
    message(WARNING "Valgrind not found on this system. Disabling Valgrind tests.")
else()
    message(STATUS "Using Valgrind: ${VALGRIND_BINARY}")
endif()

add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/third_party/googletest)
include(GoogleTest)

add_subdirectory(test_helpers)