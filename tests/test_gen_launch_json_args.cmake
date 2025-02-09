include("${CMAKE_CURRENT_LIST_DIR}/third_party/cmake-script-test-framework/cmake-test.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/../../cmake/gen_launch_json_args.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/common.cmake")

macro(setup)
endmacro()
add_setup_macro(MACRO_NAME setup)

macro(teardown)
endmacro()
add_teardown_macro(MACRO_NAME teardown)

macro(test)
    get_targets_launch_json_args("${TEST_HELPERS_DIR}/gen_targets_launch_json")
endmacro()
add_test_macro(MACRO_NAME test)