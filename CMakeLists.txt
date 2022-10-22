cmake_minimum_required(VERSION 3.12)
project(quiche VERSION 0.0.0)

find_program(CARGO cargo)
if(NOT CARGO)
  message(FATAL_ERROR "cargo not found")
endif()

find_package(Python COMPONENTS Interpreter)

# Use waf to resolve dependencies
if (NOT DEFINED STEINWURF_RESOLVE)
    message(STATUS "Resolving dependencies...")
    execute_process(
            COMMAND ${Python_EXECUTABLE} waf resolve ${STEINWURF_RESOLVE_OPTIONS}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            RESULT_VARIABLE STATUS)

    if (STATUS AND NOT STATUS EQUAL 0)
        message(FATAL_ERROR "Failed: ${STATUS}")
    endif ()

    set(STEINWURF_RESOLVE "${CMAKE_CURRENT_SOURCE_DIR}/resolve_symlinks")
    set(STEINWURF_TOP_NAME quiche)
endif()

set(QUICHE_DIR_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/resolve_symlinks/quiche-source")

execute_process(
        COMMAND ${CARGO} build --release --target-dir ${CMAKE_CURRENT_BINARY_DIR}/target
        WORKING_DIRECTORY ${QUICHE_DIR_ROOT}
        RESULT_VARIABLE STATUS)

if (${PROJECT_NAME} STREQUAL ${STEINWURF_TOP_NAME})

    install(
        FILES ${CMAKE_CURRENT_BINARY_DIR}/target/release/libquiche.a
        DESTINATION lib
        COMPONENT library
    )
else()

    find_library(quiche_shared NAMES quiche PATHS ${CMAKE_CURRENT_BINARY_DIR}/target/release NO_DEFAULT_PATH)

    set_property(GLOBAL APPEND PROPERTY steinwurf::object_libraries
        quiche_shared)
endif()

install(
        DIRECTORY ${QUICHE_DIR_ROOT}/quiche/include
        DESTINATION include
        COMPONENT headers
        FILES_MATCHING PATTERN "*.h"
)
