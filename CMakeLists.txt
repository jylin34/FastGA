# It will generate two stuff: fastga.so & run_tests(binary executable)

cmake_minimum_required(VERSION 3.14)

project(FastGA CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(pybind11 REQUIRED)

pybind11_add_module(fastga
    src/individual.cpp
    src/binding.cpp
    # add new src code as project grows
)

target_include_directories(fastga PUBLIC ${PROJECT_SOURCE_DIR}/include)


# C++ unit test (GoogleTest)

enable_testing()

include(FetchContent)

FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG    release-1.12.1 
)

FetchContent_MakeAvailable(googletest)

add_executable(
  run_tests
  tests/test_individual.cpp # to test 
  src/individual.cpp        # be tested 
  # add new src code and tes code as project grows
)

target_include_directories(run_tests PUBLIC ${PROJECT_SOURCE_DIR}/include)

target_link_libraries(
  run_tests
  PRIVATE GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(run_tests)


