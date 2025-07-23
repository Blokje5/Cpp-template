add_subdirectory (Tmp)

add_src_library (Tmp)
message(STATUS "Found the following headers:")
foreach(header IN LISTS ${PROJECT_NAME}_lib_headers)
    message(STATUS "* ${header}")
endforeach()

message(STATUS "Found the following sources:")
foreach(source IN LISTS ${PROJECT_NAME}_lib_sources)
    message(STATUS "* ${source}")
endforeach()

add_library(${PROJECT_NAME}_lib STATIC ${${PROJECT_NAME}_lib_headers} ${${PROJECT_NAME}_lib_sources})

target_include_directories(${PROJECT_NAME}_lib PUBLIC "${CMAKE_SOURCE_DIR}/src" "${CMAKE_BINARY_DIR}/src")