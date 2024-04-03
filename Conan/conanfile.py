import os

from conan             import ConanFile
from conanPackages     import conanPackages
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain

class Conan(ConanFile):
    name            = "Gpio"
    version         = "1.2"
    user            = "ssitkowx"
    channel         = "stable"
    license         = "freeware"
    repoUrl         = "https://github.com/ssitkowx"
    url             = repoUrl + '/' + name + '.git'
    description     = "General class for gpio"
    settings        = "os", "compiler", "build_type", "arch"
    options         = { "shared": [True, False] }
    default_options = { "shared": False         }
    generators      = "CMakeDeps", "CMakeToolchain"
    author          = "sylsit"
    exports         = "*"
    exports_sources = '../*'
    requires        = ["gtest/cci.20210126"]
    packagesPath    = "/home/sylwester/.conan/data"
    downloadsPath   = "/home/sylwester/.conan/download"
    packages        = []

    def layout (self):
        cmakeListsPath = os.getcwd ().replace ('/Conan','')
        cmake_layout (self, src_folder = cmakeListsPath, build_folder = cmakeListsPath + '/Build')

    def source (self):   
        conanPackages.install (self, self.downloadsPath, self.repoUrl, self.packages)

    def build (self):
        projectPath  = os.getcwd ().replace ('/Build/Release','')
        buildPath = projectPath + '/Build'
        
        if not os.path.exists (projectPath + '/CMakeLists.txt'):
            projectPath = self.downloadsPath + '/' + self.name
            buildPath   = os.getcwd () + '/Build'
        
        if self.settings.os == 'Linux' and self.settings.compiler == 'gcc':
            packagesPaths = conanPackages.getPaths (self, self.packagesPath, self.packages)
            cmake         = CMake(self)
            
            conanPath = os.getcwd () + "/PackagesProperties.txt"
            packagesPropertiesFileHandler = open (conanPath, "w")
            for packagePathKey, packagePathValue in packagesPaths.items ():
                packagesPropertiesFileHandler.writelines (packagePathKey + "=" + packagePathValue + "\n")
            packagesPropertiesFileHandler.close ()

            cmake.configure ()
            cmake.build ()
        else:
            raise Exception ('Unsupported platform or compiler')
        
    def package (self):   
        projectPath = os.getcwd ().replace ('/Conan','')
        
        if not os.path.exists (projectPath + '/CMakeLists.txt'):
            projectPath = self.downloadsPath + '/' + self.name
    
        self.copy ('*.h'     , dst = 'include', src = projectPath + '/Project' , keep_path = False)
        self.copy ('*.hxx'   , dst = 'include', src = projectPath + '/Project' , keep_path = False)
        self.copy ('*.lib'   , dst = 'lib'    , src = projectPath + '/Build/lib', keep_path = False)
        self.copy ('*.dll'   , dst = 'bin'    , src = projectPath + '/Build/bin', keep_path = False)
        self.copy ('*.dylib*', dst = 'lib'    , src = projectPath + '/Build/lib', keep_path = False)
        self.copy ('*.so'    , dst = 'lib'    , src = projectPath + '/Build/lib', keep_path = False)
        self.copy ('*.a'     , dst = 'lib'    , src = projectPath + '/Build/lib', keep_path = False)

    def package_info (self):
        self.cpp_info.libs = [self.name]
