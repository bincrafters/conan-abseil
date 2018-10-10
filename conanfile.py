#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class AbseilConan(ConanFile):
    name = "abseil"
    version = "20180600"
    commit_id = "445998d7ac4e5d3c50411d377e3b50e960d2d6c2"
    url = "https://github.com/bincrafters/conan-abseil"
    homepage = "https://github.com/abseil/abseil-cpp"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Abseil Common Libraries (C++) from Google"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    # short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    source_subfolder = "source_subfolder"
    requires = "cctz/2.2@bincrafters/stable"
    
    def source(self):
        tools.get("{0}/archive/{1}.zip".format(self.homepage, self.commit_id))
        extracted_dir = "abseil-cpp-" + self.commit_id
        os.rename(extracted_dir, self.source_subfolder)

    def configure(self):
        if self.settings.os == 'Linux':
            compiler = self.settings.compiler
            version = float(self.settings.compiler.version.value)
            libcxx = compiler.libcxx
            if compiler == 'gcc' and version > 5 and libcxx != 'libstdc++11':
                raise ConanException(
                    'Using abseil with GCC > 5 on Linux requires "compiler.libcxx=libstdc++11"'
                    'but was passed: ' + str(self.settings.compiler.libcxx))
                    
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["ABSL_CCTZ_TARGET"] = "CONAN_PKG::cctz"
        cmake.configure()
        cmake.build()
                    
    def package(self):
        self.copy("LICENSE", dst="licenses", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=self.source_subfolder)
        self.copy("*.inc", dst="include", src=self.source_subfolder)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["absl_base", "absl_synchronization", "absl_strings",
                              "absl_symbolize", "absl_malloc_internal", "absl_time",
                              "absl_strings", "absl_base", "absl_dynamic_annotations",
                              "absl_spinlock_wait", "absl_throw_delegate",
                              "absl_stacktrace", "absl_int128", "absl_span",
                              "test_instance_tracker_lib", "absl_stack_consumption", "absl_bad_any_cast",
                              "absl_hash", "str_format_extension_internal", "absl_failure_signal_handler",
                              "absl_str_format", "absl_numeric", "absl_any",
                              "absl_optional", "absl_container", "absl_debugging",
                              "absl_memory", "absl_leak_check", "absl_meta",
                              "absl_utility", "str_format_internal", "absl_variant",
                              "absl_examine_stack", "absl_bad_optional_access", "absl_algorithm"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
