cmake_minimum_required(VERSION 3.0)
project(small3d)

if(MSVC)
  add_definitions("-D_CRT_SECURE_NO_WARNINGS")
endif()

if(SMALL3D_OPENGL)
  add_compile_definitions(SMALL3D_OPENGL)
  find_package(glew)
  add_compile_definitions(${glew_COMPILE_DEFINITIONS_RELEASE})
endif()


add_subdirectory(src)
