find_package(GTest REQUIRED CONFIG)
add_subdirectory (Tmp)

macro (grep_test_sources BASE_DIR DST_VAR)
    file(GLOB_RECURSE "${DST_VAR}" CONFIGURE_DEPENDS RELATIVE "${BASE_DIR}" "test*.cpp")
endmacro()

grep_test_sources("${CMAKE_CURRENT_SOURCE_DIR}" TEST_SOURCES)

message(STATUS "Found the following test sources:")
foreach(source IN LISTS TEST_SOURCES)
    message(STATUS "* ${source}")
endforeach()

package_add_test(${PROJECT_NAME}_unit_test ${TEST_SOURCES})
