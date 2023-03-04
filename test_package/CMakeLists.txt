cmake_minimum_required(VERSION 3.0)
project(PackageTest CXX)
find_package(small3d REQUIRED)

add_executable(example src/example.cpp)
target_include_directories(example PRIVATE ${CMAKE_INCLUDE_PATH})
target_link_libraries(example PRIVATE ${small3d_LIBRARIES})
