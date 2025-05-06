cmake_minimum_required(VERSION 3.30)
include("${CMAKE_CURRENT_LIST_DIR}/../../../../../scripts/target_list_opts.cmake")
project(hello_world LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS ON)

add_executable(hello_world)
target_sources(hello_world PUBLIC hello_world.cpp)
set_source_files_properties(hello_world.cpp PROPERTIES LANGUAGE CXX)
get_source_file_property(get_prop_temp hello_world.cpp LANGUAGE)

register_target_info(hello_world)

#if(EXISTS $ENV{SET_LANGUAGE_PROPERTY})
#    set_target_properties(hello_world PROPERTIES LANGUAGES CXX)
#endif()

#if(EXISTS $ENV{SET_EXTRA_LANGUAGE_PROPERTY})
#    set_target_properties(hello_world PROPERTIES extra_language "CXX")
#endif()
