from conans import ConanFile, CMake, tools
import os
import shutil

class Box2dConan(ConanFile):
    name = "Box2D"
    version = "488beac_3"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = "CMakeLists.txt"
    requires = "multibuilder/1.0@hi3c/experimental"

    def source(self):
        tools.download("https://github.com/erincatto/Box2D/archive/{}.zip".format(self.version.split("_")[0]),
                       "box2d.zip")
        tools.unzip("box2d.zip")
        os.remove("box2d.zip")

    def build(self):
        shutil.copy("CMakeLists.txt", "Box2D-488beac0f2287ac373a72710de37d71016cd7348")

        if self.settings.arch == "universal":
            with tools.pythonpath(self):
                from multibuilder import MultiBuilder
                self.multibuilder = MultiBuilder(self, ("arm64", "x86_64"))
                self.multibuilder.multi_build(self.real_build)
                return

        self.real_build(str(self.settings.arch), "")

    def real_build(self, arch, triple):

        cmake = CMake(self)
        cmake.configure(source_dir=os.path.join(self.conanfile_directory,
                                                "Box2D-488beac0f2287ac373a72710de37d71016cd7348"),
                        build_dir=os.path.join(self.conanfile_directory, "build-" + arch))
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="Box2D-488beac0f2287ac373a72710de37d71016cd7348/Box2D")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="build-universal", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["box2d"]
