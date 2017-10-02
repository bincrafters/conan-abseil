from conans import ConanFile, tools, os
from conans.tools import os_info


class AbseilConan(ConanFile):
    name = "Abseil"
    version = "20170930"
    settings = "os", "arch"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/abseil/abseil-cpp/blob/master/LICENSE"
    options = {"with_bazel":  [True, False]}
    default_options = "with_bazel=True"
    
    def build_requirements(self):
        if self.options.with_bazel:
            self.build_requires("bazel_installer/0.6.0@bincrafters/testing")
        
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        self.run("git clone --depth=1 {0}.git".format(source_url))
        
    def build(self):
        with tools.chdir("./abseil-cpp"):
            if os_info.is_windows:
                if str(self.settings.arch) == "x86":
                    self.output.info("using 32bit for bazel")
                    self.run("bazel --batch build --cpu=x86_windows_msvc absl/...:all")
                else:
                    self.output.info("using 64bit for bazel")
                    self.run("bazel --batch build --cpu=x64_windows_msvc absl/...:all")
            else: 
                self.run("bazel --batch build absl/...:all")
                    
    def package(self):
        abseil_root = os.path.join("abseil-cpp", "bazel-abseil-cpp")
        out_dir = os.path.join(abseil_root, "bazel-out")
        self.copy("*.h", dst="include",  src=abseil_root, excludes="external")
        self.copy("*.lib", dst="lib", src=out_dir, excludes="external", keep_path=False)
        self.copy("*.dll", dst="bin", src=out_dir, excludes="external", keep_path=False)
        self.copy("*.dylib*", dst="lib", src=out_dir, excludes="external", keep_path=False)
        self.copy("*.so", dst="lib", src=out_dir, excludes="external", keep_path=False)
        self.copy("*.a", dst="lib", src=out_dir, excludes="external", keep_path=False)

    def package_info(self):
        tools.collect_libs(self)

