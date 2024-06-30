
cmake_minimum_required(VERSION 3.22)

add_library(cmpr_add_warnings INTERFACE)
add_library(cmpr::add_warnings ALIAS cmpr_add_warnings)

set(PRESET_WARNINGS "" CACHE STRING "You may set this to whatever you like to add to your own library as warning compile options")

target_compile_options(cmpr_add_warnings INTERFACE ${PRESET_WARNINGS})
