cmake_minimum_required(VERSION 3.0)
project(small3d)

if(MSVC)
  add_definitions("-D_CRT_SECURE_NO_WARNINGS")
endif()

add_subdirectory(src)
