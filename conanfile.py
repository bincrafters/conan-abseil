from conans import ConanFile, tools, os
from conans.tools import os_info


class AbseilConan(ConanFile):
    name = "Abseil"
    version = "20170930"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/abseil/abseil-cpp/blob/master/LICENSE"
    short_paths = True
    options = {"with_bazel":  [True, False]}
    default_options = "with_bazel=True"
    
    def build_requirements(self):
        if self.options.with_bazel:
            self.build_requires("bazel_installer/0.6.0@bincrafters/stable")
        
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        self.run("git clone --depth=1 {0}.git".format(source_url))
        
    def build(self):
        
        with tools.chdir("./abseil-cpp"):
            if os_info.is_windows:
                if str(self.settings.arch) == "x86":
                    self.output.info("using 32bit for bazel")
                    cpu="x86_windows_msvc"
                else:
                    self.output.info("using 64bit for bazel")
                    cpu="x64_windows_msvc"
                    
                cmd_prefix = "bazel --batch build --cpu={0}".format(cpu)
            else:
                cmd_prefix = "bazel --batch build"
            
            self.run(cmd_prefix + " absl/...:all")
                    
    def package(self):
        abseil_root = os.path.join("abseil-cpp", "bazel-abseil-cpp")
        out_dir = os.path.join(abseil_root, "bazel-out")
        self.copy("*.h", dst="include", src=abseil_root, excludes="*external*")
        self.copy("*.a", dst="lib", src=out_dir, keep_path=False)

    def package_info(self):
        tools.collect_libs(self)

