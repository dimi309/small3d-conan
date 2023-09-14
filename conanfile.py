from conan import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.files import copy, collect_libs, get
import os
import shutil

class Small3dConan(ConanFile):
    name = "small3d"
    license = "BSD 3-Clause"
    version = "master"
    author = "dimi309"
    url = "https://github.com/dimi309/small3d-conan"
    description = "Minimalistic, open source library for making 3D games in C++"
    topics = ("small3d", "opengl", "gamedev")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # WARNING: There is an issue with the conan build of freetype/2.12.1 so it is not being used.
    requires = "bzip2/1.0.8", "freetype/2.11.1", "glfw/3.3.8", "glm/0.9.9.8", "libpng/1.6.40", "vorbis/1.3.7", "zlib/1.2.13", "portaudio/19.7.0", "glew/2.2.0", "cereal/1.3.2"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "cmakefiles/CMakeLists.txt", "cmakefiles/src.CMakeLists.txt", "src*", "include*", "scripts*", "resources*", "LICENSE"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
   
    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        shutil.copy("cmakefiles/src.CMakeLists.txt", "src/CMakeLists.txt")
        shutil.copy("cmakefiles/CMakeLists.txt", "CMakeLists.txt")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()
        
    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "*", dst=os.path.join(self.package_folder, "bin/resources/shaders"), src=os.path.join(self.source_folder, "resources/shaders"))
        copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))

        copy(self, pattern="*.lib", dst=os.path.join(self.package_folder, "lib"), src=self.source_folder, keep_path=False)
        copy(self, pattern="*.a", dst=os.path.join(self.package_folder, "lib"), src=self.source_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
