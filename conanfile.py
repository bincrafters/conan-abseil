#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os


class AbseilConan(ConanFile):
    name = "abseil"
    version = "20171101"
    commit_id = "c56e7827d6657f351dd2639b0224afa96f3a68d4"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    short_paths = True
    settings = "os", "arch", "compiler", "build_type"

    source_subfolder = "source_subfolder"
    
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        tools.get("{0}/archive/{1}.zip".format(source_url, self.commit_id))
        extracted_dir = "abseil-cpp-" + self.commit_id
        os.rename(extracted_dir, self.source_subfolder)
                       
    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run("bazel --batch build absl/...:all")
                    
    def package(self):
        abseil_root = os.path.join(self.source_subfolder, "bazel-abseil-cpp")
        out_dir = os.path.join(abseil_root, "bazel-out")
        self.copy("LICENSE", src=self.source_subfolder)
        self.copy("*.h", dst="include", src=abseil_root, excludes="*external*")
        self.copy("*.a", dst="lib", src=out_dir, keep_path=False)

    def package_info(self):
        tools.collect_libs(self)