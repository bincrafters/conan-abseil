#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

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
                raise ConanInvalidConfiguration(
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
        if self.settings.os != "Windows":
            self.cpp_info.libs = ["-Wl,--start-group"]

        self.cpp_info.libs.extend(tools.collect_libs(self))

        if self.settings.os != "Windows":
            self.cpp_info.libs.append("-Wl,--end-group")

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
