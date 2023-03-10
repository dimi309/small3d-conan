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
    description = "Minimalistic, open source library for making 3D games in C++, with Vulkan and OpenGL support"
    topics = ("small3d", "opengl", "vulkan", "gamedev")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "vulkan": [True, False]}
    default_options = {"shared": False, "fPIC": True, "vulkan": False}

    # WARNING: There is an issue with the conan build of freetype/2.12.1 so it is not being used.
    requires = "bzip2/1.0.8", "freetype/2.11.1", "glfw/3.3.8", "glm/0.9.9.8", "libpng/1.6.39", "vorbis/1.3.7", "zlib/1.2.13", "portaudio/19.7.0"

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "cmakefiles/CMakeLists.txt", "cmakefiles/src.CMakeLists.txt", "src*", "include*", "scripts*", "resources*", "opengl*", "LICENSE"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.options.vulkan:
            self.requires("vulkan-loader/1.3.239.0")
            self.requires("vulkan-headers/1.3.239.0")
        else:
            self.requires("glew/2.2.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        shutil.copy("cmakefiles/src.CMakeLists.txt", "src/CMakeLists.txt")
        shutil.copy("cmakefiles/CMakeLists.txt", "CMakeLists.txt")

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        if not self.options.vulkan:
            tc.variables["SMALL3D_OPENGL"] = True
        tc.generate()
        
    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        
        cmake.configure()
        cmake.build()
        if self.options.vulkan:
            if self.settings.os == "Windows":
                self.run("cd ..\\scripts && compile-shaders.bat " + str(self.settings.build_type))
            else:
                if self.settings.build_type == "Release":
                    debug_info = "-g0"
                else:
                    debug_info = "-g"
                self.run("cd ../../resources/shaders && glslangValidator -V perspectiveMatrixLightedShader.vert -o perspectiveMatrixLightedShader.spv "+ debug_info +
                             " && glslangValidator -V textureShader.frag -o textureShader.spv " + debug_info)

    def package(self):
        if self.options.vulkan:
            copy(self, pattern="*.spv", dst=os.path.join(self.package_folder, "bin/resources"), src=os.path.join(self.source_folder, "resources"))
            copy(self, pattern="*.hpp", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"))
        else:
            copy(self, "*", dst=os.path.join(self.package_folder, "bin/resources/shaders"), src=os.path.join(self.source_folder, "opengl/resources/shaders"))
            copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "include"), excludes="Renderer.*p")
            copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "opengl/include"))

        copy(self, pattern="*.lib", dst=os.path.join(self.package_folder, "lib"), src=self.source_folder, keep_path=False)
        copy(self, pattern="*.a", dst=os.path.join(self.package_folder, "lib"), src=self.source_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        if not self.options.vulkan:
            self.cpp_info.defines = ["SMALL3D_OPENGL"]
