add_subdirectory("${PROJECT_SOURCE_DIR}/extern/googletest" "extern/googletest")
add_subdirectory (Tmp)

mark_as_advanced(
    BUILD_GMOCK BUILD_GTEST BUILD_SHARED_LIBS
    gmock_build_tests gtest_build_samples gtest_build_tests
    gtest_disable_pthreads gtest_force_shared_crt gtest_hide_internal_symbols
)
set_target_properties(gtest PROPERTIES FOLDER extern)
set_target_properties(gtest_main PROPERTIES FOLDER extern)
set_target_properties(gmock PROPERTIES FOLDER extern)
set_target_properties(gmock_main PROPERTIES FOLDER extern)

macro (grep_test_sources BASE_DIR DST_VAR)
    file(GLOB_RECURSE "${DST_VAR}" CONFIGURE_DEPENDS RELATIVE "${BASE_DIR}" "test*.cpp")
endmacro()

grep_test_sources("${CMAKE_CURRENT_SOURCE_DIR}" TEST_SOURCES)

message(STATUS "Found the following test sources:")
foreach(source IN LISTS TEST_SOURCES)
    message(STATUS "* ${source}")
endforeach()

package_add_test(${PROJECT_NAME}_unit_test ${TEST_SOURCES})