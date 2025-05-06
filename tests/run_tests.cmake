include("${CMAKE_CURRENT_LIST_DIR}/third_party/cmake-script-test-framework/cmake-test-runner.cmake")

run_test(
    TEST_SCRIPT_FILE "${CMAKE_CURRENT_LIST_DIR}/test_target_list_opts.cmake"   
)

