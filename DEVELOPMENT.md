# Building the project
This C++ template relies on [Conan 2](https://conan.io/) to manage dependencies and [CMake](https://cmake.org/) to handle builds.

To compile the project, first install the dependencies into a build directory (for example, a Clang build directory):

```console
conan profile detect --force
CC=clang-20 CXX=clang++ conan install . --output-folder=build-clang --build=missing -s build_type=RelWithDebInfo
```

Then configure CMake using the Conan-generated toolchain:

```console
CC=clang-20 CXX=clang++ cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja -S . -B build-clang -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_TOOLCHAIN_FILE=build-clang/conan_toolchain.cmake
```

This initialises CMake to use clang. `clang-20` is used to support features from `c++23`.

To compile the project:

```console
cmake --build build-clang -j 1
```

# Code Formatting

This project uses [clang-format](https://clang.llvm.org/docs/ClangFormat.html) for C++ code style.

A custom CMake target is available to format all source files. After configuring CMake, the target can be run with:

```console
cmake --build build-clang --target clang_format -j 1
```

By default, CMake will try to find `clang-format` in your `PATH`.
If you have `clang-format` installed at a custom location, specify it when configuring:

```console
-DCLANG_FORMAT_BIN=/path/to/clang-format
```

When running the CMake command.

This will ensure the correct `clang-format` binary is used for formatting.

# Linting

Linting can be done with clang-tidy:

```console
CC=clang-20 CXX=clang++ conan install . --output-folder=build-tidy --build=missing -s build_type=Debug
```

```console
CC=clang-20 CXX=clang++ cmake -G Ninja -S . -B build-tidy -D{PROJECT_NAME}_ENABLE_CLANG_TIDY -DCMAKE_TOOLCHAIN_FILE=build-tidy/conan_toolchain.cmake
```

```console
cmake --build build-tidy -j4
```

# Compiling with sanitizers

To create a build with sanitizers enabled:

```console
CC=clang-20 CXX=clang++ conan install . --output-folder=build-clang-debug --build=missing -s build_type=Debug
```

```console
CC=clang-20 CXX=clang++ cmake -DCMAKE_BUILD_TYPE=Debug -G Ninja -S . -B build-clang-debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -D{PROJECT_NAME}_ENABLE_ASAN=ON -D{PROJECT_NAME}_ENABLE_UBSAN=ON -D{PROJECT_NAME}_ENABLE_MSAN=ON -DCMAKE_TOOLCHAIN_FILE=build-clang-debug/conan_toolchain.cmake
```

```console
cmake --build build-clang-debug -j4
```

# Testing

Unit Tests are compiled when building the project. You can run the unit tests by running:

```console
./build-clang/test/{PROJECT_NAME}_unit_test
```

You can specifically target the unit test target with:

```
cmake --build build-clang --target ${PROJECT_NAME}_unit_test
```

# Adding dependencies

Dependencies are added in `conanfile.py` and then consumed from CMake with `find_package(...)` and imported targets.

For example, GoogleTest is declared as:

```python
requires = "gtest/1.17.0"
```

After editing `conanfile.py`, rerun `conan install` for the build directory you want to use so CMake can resolve the generated package configuration files.

In CMake, dependencies should be linked via their package targets. For GoogleTest:

```console
find_package(GTest REQUIRED CONFIG)
target_link_libraries(your_target PRIVATE GTest::gtest GTest::gmock GTest::gtest_main)
```
