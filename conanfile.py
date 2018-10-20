#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os


class AbseilConan(ConanFile):
    name = "abseil"
    version = "20180223"
    _commit_id = "0d40cb771eec8741f44e5979cfccf1eeeedb012a"
    url = "https://github.com/bincrafters/conan-abseil"
    homepage = "https://github.com/abseil/abseil-cpp"
    description = "Abseil Common Libraries (C++) from Google"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    # short_paths = True
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    _source_subfolder = "source_subfolder"
    requires = "cctz/2.2@bincrafters/stable"
    
    def source(self):
        tools.get("{0}/archive/{1}.zip".format(self.homepage, self._commit_id))
        extracted_dir = "abseil-cpp-" + self._commit_id
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        if self.settings.os == 'Windows':
            if self.settings.compiler == "Visual Studio" and \
               float(self.settings.compiler.version.value) < 14:
                raise ConanInvalidConfiguration("Abseil requires Visual Studio >= 14")
                    
    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["ABSL_CCTZ_TARGET"] = "CONAN_PKG::cctz"
        cmake.configure()
        cmake.build()
                    
    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy("*.h", dst="include", src=self._source_subfolder)
        self.copy("*.inc", dst="include", src=self._source_subfolder)
        self.copy("*.a", dst="lib", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
            "absl_base",
            "absl_synchronization",
            "absl_strings",
            "absl_malloc_internal",
            "absl_time",
            "absl_strings",
            "absl_base",
            "absl_dynamic_annotations",
            "absl_spinlock_wait",
            "absl_throw_delegate",
            "absl_stacktrace",
            "absl_int128",
            "absl_span",
            "test_instance_tracker_lib",
            "absl_stack_consumption",
            "absl_bad_any_cast",
            "absl_numeric",
            "absl_any",
            "absl_optional",
            "absl_container",
            "absl_debugging",
            "absl_memory",
            "absl_leak_check",
            "absl_meta",
            "absl_utility",
            "absl_bad_optional_access",
            "absl_algorithm"
        ]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
