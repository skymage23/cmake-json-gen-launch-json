include("${CMAKE_CURRENT_LIST_DIR}/../../../scripts/target_list_opts.cmake")

add_subdirectory("custom_targets")
add_subdirectory("tests")

write_targets_list_file()