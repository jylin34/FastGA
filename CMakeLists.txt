cmake_minimum_required(VERSION 3.14)

project(FastGA)

set(CMAKE_COMPILE_WARNING_AS_ERROR ON)

# GoogleTest requires at least C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# =========================== Dependencies Setup ===========================

include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v3.0.4
)
FetchContent_MakeAvailable(pybind11)

find_package(Python COMPONENTS Development REQUIRED)

FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# ============================== Core Library ==============================

# make static library prevent recompiling same src code
add_library(FastGA_core STATIC)
set_target_properties(FastGA_core PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_sources(FastGA_core
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src/individual.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/ga_solver.cpp
)

target_include_directories(FastGA_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${Python_INCLUDE_DIRS}   # from find_package(Python)
)

target_link_libraries(FastGA_core
    PUBLIC
        pybind11::headers
        ${Python_LIBRARIES}      # from find_package(Python)
)

# ============================== Executable ==============================

add_executable(FastGA_exec)

target_sources(FastGA_exec
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
)

target_link_libraries(FastGA_exec
    PRIVATE
        FastGA_core
)

# ============================== pybind11 ==============================

pybind11_add_module(
    fastga
    ${CMAKE_CURRENT_SOURCE_DIR}/src/binding.cpp
    # add new src code as project grows
)

target_link_libraries(
    fastga
    PRIVATE
        FastGA_core
)

# ============================== GoogleTest ==============================

# https://google.github.io/googletest/quickstart-cmake.html#set-up-a-project
enable_testing()

add_executable(unit_test)

target_sources(unit_test 
    PRIVATE 
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/unit/test_individual.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/unit/test_fitness_function.cpp
)

target_link_libraries(
    unit_test
    PRIVATE
        FastGA_core
        GTest::gtest_main
        pybind11::embed
)

include(GoogleTest)
gtest_discover_tests(unit_test)
