macro(add_glob cur_list)
    file(GLOB __tmp CONFIGURE_DEPENDS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${ARGN})
    list(APPEND ${cur_list} ${__tmp})
endmacro()

macro(add_headers_and_sources prefix common_path)
    message(STATUS "Adding headers and sources from: ${common_path} under prefix: ${prefix}")
    add_glob(${prefix}_headers ${common_path}/*.h)
    add_glob(${prefix}_sources ${common_path}/*.cpp ${common_path}/*.c)
endmacro()

macro(add_src_library common_path)
    add_headers_and_sources(${PROJECT_NAME}_lib ${common_path})
endmacro()