
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../../../../../../../tests/third_party/googletest)
include(GoogleTest)


add_executable(test_hello_world test_hello_world.cpp)
target_link_libraries(test_hello_world
   PUBLIC hello_world
   PUBLIC GTest::gtest_main
)