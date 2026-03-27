# Building the project
This C++ template relies on [Conan 2](https://conan.io/) to manage dependencies and [CMake](https://cmake.org/) to handle builds.

## Configure with Conan presets

The default workflow is:

```console
conan profile detect --force
conan install . --output-folder=build/default --build=missing -s build_type=RelWithDebInfo
cmake --preset conan-relwithdebinfo
cmake --build --preset conan-relwithdebinfo
```

`conan install` generates:

- `build/<name>/build/<BuildType>/generators/CMakePresets.json`
- `build/<name>/build/<BuildType>/generators/conan_toolchain.cmake`
- `CMakeUserPresets.json` at the repository root

With CMake 3.23 or newer, `CMakeUserPresets.json` makes the Conan-generated presets available through `cmake --preset ...`.

The generated preset names follow the build type for single-config generators:

- `conan-debug`
- `conan-release`
- `conan-relwithdebinfo`
- `conan-minsizerel`

If you rerun `conan install` with a different `--output-folder`, Conan rewrites `CMakeUserPresets.json` to point at that build folder. In practice this means: run `conan install` for the build variant you want, then use the matching `cmake --preset ...` and `cmake --build --preset ...` commands.

If you want a different CMake generator such as Ninja, set it during `conan install`. For example:

```console
conan install . --output-folder=build/default --build=missing -s build_type=RelWithDebInfo -c tools.cmake.cmaketoolchain:generator=Ninja
```

## Configure without presets

If you prefer the explicit toolchain flow, it still works:

```console
conan install . --output-folder=build/default --build=missing -s build_type=RelWithDebInfo
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -G Ninja -S . -B build/default -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_TOOLCHAIN_FILE=build/default/conan_toolchain.cmake
```

To compile the project:

```console
cmake --build build/default -j 1
```

# Code Formatting

This project uses [clang-format](https://clang.llvm.org/docs/ClangFormat.html) for C++ code style.

A custom CMake target is available to format all source files. After configuring CMake, the target can be run with:

```console
cmake --build build/default --target clang_format -j 1
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
conan install . --output-folder=build/tidy --build=missing -s build_type=Debug -o '&:with_clang_tidy=True'
```

```console
cmake --preset conan-debug
```

```console
cmake --build --preset conan-debug -j4
```

# Compiling with sanitizers

To create a build with sanitizers enabled:

```console
conan install . --output-folder=build/asan --build=missing -s build_type=Debug -o '&:with_asan=True' -o '&:with_ubsan=True'
```

```console
cmake --preset conan-debug
```

```console
cmake --build --preset conan-debug -j4
```

# Testing

Unit Tests are compiled when building the project. You can run the unit tests by running:

```console
./build/default/test/{PROJECT_NAME}_unit_test
```

You can specifically target the unit test target with:

```
cmake --build build/default --target ${PROJECT_NAME}_unit_test
```

# Adding dependencies

Dependencies are added in `conanfile.py` and then consumed from CMake with `find_package(...)` and imported targets.

`conanfile.py` is split into two lists:

- `project_requirements` for dependencies used by the application or library itself
- `project_test_requirements` for dependencies only used by tests

For example:

```python
project_requirements = (
    "fmt/11.2.0",
)

project_test_requirements = (
    "gtest/1.17.0",
)
```

To add a new dependency:

1. Add the Conan package reference to the appropriate tuple in `conanfile.py`.
2. Rerun `conan install` for the build directory you want to use.
3. Add `find_package(... REQUIRED CONFIG)` in the relevant `CMakeLists.txt`.
4. Link the imported target with `target_link_libraries(...)`.

For a normal library dependency such as `fmt`:

```cmake
find_package(fmt REQUIRED CONFIG)
target_link_libraries(${PROJECT_NAME}_lib PRIVATE fmt::fmt)
```

For GoogleTest, which is only used by tests in this template:

```cmake
find_package(GTest REQUIRED CONFIG)
target_link_libraries(your_target PRIVATE GTest::gtest GTest::gmock GTest::gtest_main)
```

The Conan package name and the CMake package or target names are not always identical. Check the package page on ConanCenter if you are unsure which `find_package(...)` name or imported target to use.

After changing dependencies, rerun `conan install` before reconfiguring CMake so the generated dependency files stay in sync with `conanfile.py`.

# Build variants

The Conan recipe exposes project-level options that are written into the generated CMake presets as cache variables:

- `with_unit_tests`
- `with_clang_tidy`
- `with_asan`
- `with_ubsan`
- `with_msan`

That means the preset flow still supports clang, ASAN, and MSAN builds, but the compiler choice belongs in the Conan profile and the sanitizer choice belongs in the Conan options.

For a Clang build, use a Conan profile that selects Clang and points Conan at the Clang executables. For example:

```ini
[settings]
compiler=clang
compiler.version=20
compiler.cppstd=gnu23
compiler.libcxx=libstdc++11

[conf]
tools.build:compiler_executables={"c": "clang-20", "cpp": "clang++"}
```

Then install and build with presets:

```console
conan install . --output-folder=build/clang-debug --build=missing -pr:h=/path/to/clang20 -pr:b=default -s build_type=Debug
cmake --preset conan-debug
cmake --build --preset conan-debug
```

For a Clang ASAN/UBSAN build:

```console
conan install . --output-folder=build/clang-asan --build=missing -pr:h=/path/to/clang20 -pr:b=default -s build_type=Debug -o '&:with_asan=True' -o '&:with_ubsan=True'
cmake --preset conan-debug
cmake --build --preset conan-debug
```

For a Clang MSAN build:

```console
conan install . --output-folder=build/clang-msan --build=missing -pr:h=/path/to/clang20 -pr:b=default -s build_type=Debug -o '&:with_msan=True'
cmake --preset conan-debug
cmake --build --preset conan-debug
```

MSAN generally requires Clang and instrumented dependencies. In this template that is feasible because Conan builds dependencies such as `gtest` for the selected profile instead of relying on a prebuilt submodule checkout. This is an inference from the toolchain setup and Conan dependency model.
