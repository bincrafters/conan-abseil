from conans import ConanFile, tools, os
from conans.tools import os_info, SystemPackageTool, ChocolateyTool

class AbseilConan(ConanFile):
    name = "Abseil"
    version = "20170930"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-abseil"
    description = "Abseil Common Libraries (C++) from Google"
    license = "https://github.com/abseil/abseil-cpp/blob/master/LICENSE"
    options = {"shared": [True, False], "with_msys2":  [True, False], "with_bazel":  [True, False], "with_java8": [True, False]}
    default_options = "shared=False", "with_msys2=False", "with_bazel=False", "with_java8=False"
    
    def system_requirements(self):
        package_name = "bazel"
        if os_info.is_windows:
            installer = SystemPackageTool(tool=ChocolateyTool())
            installer.install(" ".join(["msys2", package_name]))
        elif os_info.linux_distro == "ubuntu":
            tools.save("/etc/apt/sources.list.d/bazel.list", "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8")
            key_file = "bazel-release.pub.gpg"
            if os.path.isfile(key_file): 
                os.remove(key_file)
            tools.download("https://bazel.build/bazel-release.pub.gpg", key_file)
            self.run("apt-key add " + key_file)
            installer = SystemPackageTool()
            installer.install(" ".join(["openjdk-8-jdk", package_name]))
        elif os_info.linux_distro == "fedora":
            self.run("dnf copr enable vbatts/bazel")
            installer = SystemPackageTool()
            installer.install(" ".join(["openjdk-8-jdk", package_name]))
        elif os_info.linux_distro == "centos":
            repo_file = "vbatts-bazel-epel-7.repo"
            if os.path.isfile(repo_file): 
                os.remove(repo_file)
            tools.download("https://copr.fedorainfracloud.org/coprs/vbatts/bazel/repo/epel-7/vbatts-bazel-epel-7.repo", repo_file)
            installer = SystemPackageTool()
            installer.install(" ".join(["java-1.8.0-openjdk", package_name]))
        elif os_info.is_macos:
            installer = SystemPackageTool()
            installer.install(" ".join(["java8", package_name]))            
        
    def source(self):
        source_url = "https://github.com/abseil/abseil-cpp"
        self.run("git clone --depth=1 {0}.git".format(source_url))
        
    def build(self):
        with tools.chdir("./abseil-cpp"):
            if os_info.is_windows:
                if str(self.settings.arch) == "x86":
                    self.output.info("using 32bit for bazel")
                    self.run("bazel --batch build --batch --cpu=x86_windows_msvc absl/...:all")
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

