from conan import ConanFile
from conan.tools.cmake import cmake_layout


class ProjectConan(ConanFile):
    name = "project"
    version = "0.1.0"

    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    requires = "gtest/1.17.0"

    def layout(self):
        cmake_layout(self)
