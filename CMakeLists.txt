
cmake_minimum_required(VERSION 3.22)

add_library(cmpr_add_warnings INTERFACE)
add_library(cmpr::add_warnings ALIAS cmpr_add_warnings)

set(PRESET_WARNINGS "" CACHE STRING "You may set this to whatever you like to add to your own library as warning compile options")

target_compile_options(cmpr_add_warnings INTERFACE ${PRESET_WARNINGS})

set(PRESET_ADDRSAN OFF CACHE BOOL "Set to true to use address sanitizer")

if (PRESET_ADDRSAN)
    if (${CMAKE_CXX_COMPILER_ID} STREQUAL MSVC)
        cmake_path(GET CMAKE_CXX_COMPILER PARENT_PATH PRESET_ADDRSAN_PATH)
        set(PRESET_ADDRSAN_PATH "${PRESET_ADDRSAN_PATH}/clang_rt.asan_dynamic-x86_64.dll")
        file(COPY "${PRESET_ADDRSAN_PATH}" DESTINATION ".")
        target_compile_options(cmpr_add_warnings INTERFACE "/fsanitize=address")
    endif ()
endif ()
