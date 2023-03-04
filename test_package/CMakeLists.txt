cmake_minimum_required(VERSION 3.0)
project(PackageTest CXX)
find_package(small3d REQUIRED)

get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()

add_executable(example src/example.cpp)

target_link_libraries(example small3d_LIBRARIES)
