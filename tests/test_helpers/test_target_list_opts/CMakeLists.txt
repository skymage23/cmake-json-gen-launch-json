cmake_minimum_required(VERSION 3.20)
project(hello_world)
include("${CMAKE_CURRENT_LIST_DIR}/../../../scripts/target_list_opts.cmake")

add_subdirectory("custom_targets")

if(EXISTS ${OUTPUT_FILE_PATH})
    set(file_path "${OUTPUT_FILE_PATH}")
else()
    set(file_path "${CMAKE_BINARY_DIR}/CMakeFiles/CMakeScratch/target_list.txt")
endif()
file(REMOVE ${file_path})
gen_target_list_file(OUTPUT_FILE ${file_path})