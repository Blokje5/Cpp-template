cmake_minimum_required(VERSION 3.27)

# Project Definition
project(
  "Project"
  VERSION 0.1.0
  LANGUAGES CXX
)

# Project Options
# Includes for CMake
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
# Default language settings
include(LanguageSettings)
# Static Analysis, Formatting, and other tools
include(Format)
include(StaticAnalysis)
include(UnitTesting)
include(Glob)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Debug")
endif()
message(STATUS "Started CMake ${CMAKE_BUILD_TYPE} Build for ${PROJECT_NAME} v${PROJECT_VERSION}...\n")

if (UNIX)
    add_compile_options("$<$<CONFIG:DEBUG>:-D_DEBUG>")    #this will allow to use same _DEBUG macro available in both Linux as well as Windows - MSCV environment. Easy to put Debug specific code.
endif (UNIX)

# Prevent building in the source directory
if(PROJECT_SOURCE_DIR STREQUAL PROJECT_BINARY_DIR)
  message(FATAL_ERROR "In-source builds not allowed. Please make a new directory (called a build directory) and run CMake from there.\n")
endif()

############################################################
######################   Executable   ######################
############################################################
add_subdirectory(src)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${PROJECT_NAME}_lib)

############################################################
######################   Test Build   ######################
############################################################

if(${PROJECT_NAME}_ENABLE_UNIT_TESTING )
    enable_testing()
    include(GoogleTest)
    add_subdirectory(test)
endif()