from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout


class ProjectConan(ConanFile):
    name = "project"
    version = "0.1.0"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "with_unit_tests": [True, False],
        "with_clang_tidy": [True, False],
        "with_asan": [True, False],
        "with_ubsan": [True, False],
        "with_msan": [True, False],
    }
    default_options = {
        "with_unit_tests": True,
        "with_clang_tidy": False,
        "with_asan": False,
        "with_ubsan": False,
        "with_msan": False,
    }

    # Add production dependencies here, for example:
    # project_requirements = ("fmt/11.2.0",)
    project_requirements = ()

    # Add test-only dependencies here.
    project_test_requirements = ("gtest/1.17.0",)

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        for requirement in self.project_requirements:
            self.requires(requirement)

    def test_requirements(self):
        if self.options.with_unit_tests:
            for requirement in self.project_test_requirements:
                self.test_requires(requirement)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["PROJECT_ENABLE_UNIT_TESTING"] = self.options.with_unit_tests
        tc.cache_variables["PROJECT_USE_GTEST"] = self.options.with_unit_tests
        tc.cache_variables["PROJECT_ENABLE_CLANG_TIDY"] = self.options.with_clang_tidy
        tc.cache_variables["PROJECT_ENABLE_ASAN"] = self.options.with_asan
        tc.cache_variables["PROJECT_ENABLE_UBSAN"] = self.options.with_ubsan
        tc.cache_variables["PROJECT_ENABLE_MSAN"] = self.options.with_msan
        tc.generate()
