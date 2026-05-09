cmake_minimum_required(VERSION 3.14)

project(FastGA)

# GoogleTest requires at least C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================== Core Library ==============================

# make static library prevent recompiling same src code
add_library(
    fastga_core
    STATIC
    src/individual.cpp
    # add new src code as project grows
)

target_include_directories(
    fastga_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(
    FastGA
    src/main.cpp
)

target_link_libraries(
    FastGA
    PRIVATE
        fastga_core
)

# ============================== pybind11 ==============================

find_package(pybind11 REQUIRED)

pybind11_add_module(
    fastga
    src/binding.cpp
    # add new src code as project grows
)

target_link_libraries(
    fastga
    PRIVATE
        fastga_core
)

# ============================== GoogleTest ==============================

# https://google.github.io/googletest/quickstart-cmake.html#set-up-a-project

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(
    unit_test 
    tests/unit/test_individual.cpp
)

target_link_libraries(
    unit_test
    PRIVATE
        fastga_core
        GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(unit_test)
