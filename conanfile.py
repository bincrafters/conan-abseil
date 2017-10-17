from conans import ConanFile, tools, os


class AbseilConan(ConanFile):
    name = "Abseil"
    version = "20171012"
    commit_id = "1a9ba5e2e5a14413704f0c913fac53359576d3b6"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/abseil/abseil-cpp/blob/master/LICENSE"
    short_paths = True
    options = {"with_bazel":  [True, False]}
    default_options = "with_bazel=True"
    
    def build_requirements(self):
        if self.options.with_bazel:
            self.build_requires("bazel_installer/0.6.0@bincrafters/testing")
        
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        self.run("git clone --depth=1 {0}.git".format(source_url))
        with tools.chdir("./abseil-cpp"):
            self.run("git checkout {0}".format(self.commit_id))
                
    def build(self):
        with tools.chdir("./abseil-cpp"):
            self.run("bazel --batch build absl/...:all")
                    
    def package(self):
        abseil_root = os.path.join("abseil-cpp", "bazel-abseil-cpp")
        out_dir = os.path.join(abseil_root, "bazel-out")
        self.copy("*.h", dst="include", src=abseil_root, excludes="*external*")
        self.copy("*.a", dst="lib", src=out_dir, keep_path=False)

    def package_info(self):
        tools.collect_libs(self)
    def package_id(self):
        self.info.options.with_bazel = "any" 
