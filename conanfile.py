from conans import ConanFile, CMake, tools
import os
import shutil

class Box2dConan(ConanFile):
    name = "Box2D"
    version = "488beac"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    exports = "CMakeLists.txt"

    def source(self):
        tools.download("https://github.com/erincatto/Box2D/archive/{}.zip".format(self.version),
                       "box2d.zip")
        tools.unzip("box2d.zip")
        os.remove("box2d.zip")

    def build(self):
        shutil.copy("CMakeLists.txt", "Box2D-488beac0f2287ac373a72710de37d71016cd7348")

        cmake = CMake(self)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake Box2D-{} {} {}'.format("488beac0f2287ac373a72710de37d71016cd7348", cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="Box2D-488beac0f2287ac373a72710de37d71016cd7348/Box2D")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["box2d"]
