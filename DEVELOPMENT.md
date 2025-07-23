# Building the project
This c++ template relies on [CMake](https://cmake.org/) to handle builds.

To compile the project, first setup a build directory (e.g. a build directory for Clang):

```console
CXX=clang++ CC=clang-20 cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja -S . -B build-clang -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
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
CXX=clang++ CC=clang-20 cmake -G Ninja -S . -B build-tidy  -D{PROJECT_NAME}_ENABLE_CLANG_TIDY
```

```console
cmake --build build-tidy -j4
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

Dependencies are added as a submodule. Make sure to select a specific version of the Dependency. E.g. for GoogleTest:

```console
git submodule add -b v1.17.x https://github.com/google/googletest.git extern/googletest
```

To initialise and update the submodules:

```console
git submodule update --init --recursive
```
