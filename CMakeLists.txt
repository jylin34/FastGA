cmake_minimum_required(VERSION 3.14)

project(FastGA)

# GoogleTest requires at least C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================== Core Library ==============================

# make static library prevent recompiling same src code
add_library(FastGA_core STATIC)

target_sources(FastGA_core
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src/individual.cpp
)

target_include_directories(FastGA_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# ============================== Executable ==============================

add_executable(FastGA)

target_sources(FastGA
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
)

target_link_libraries(FastGA
    PRIVATE
        FastGA_core
)

# ============================== pybind11 ==============================

find_package(pybind11 REQUIRED)

pybind11_add_module(
    FastGA_mod
    ${CMAKE_CURRENT_SOURCE_DIR}/src/binding.cpp
    # add new src code as project grows
)

target_link_libraries(
    FastGA_mod
    PRIVATE
        FastGA_core
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

add_executable(unit_test)

target_sources(unit_test 
    PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/unit/test_individual.cpp
)

target_link_libraries(
    unit_test
    PRIVATE
        FastGA_core
        GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(unit_test)
