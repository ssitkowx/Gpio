import os

from conan             import ConanFile
from conanPackages     import conanPackages
from conan.tools.files import copy, load
from conan.tools.cmake import CMake, cmake_layout

from conan.tools.scm   import Git

class Conan(ConanFile):
    name            = "gpio"
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
    exports_sources = "CMakeLists.txt", "Project/*"
    #requires        = ["Utils/1.1@ssitkowx/stable"]
    requires        = ["gtest/cci.20210126"]
    downloadPath    = "/home/sylwester/.conan2/download"
    repoPath        = downloadPath + '/Repo'
    packagePath     = downloadPath + '/Package'
    #packages        = ["Utils/1.1@ssitkowx/stable"]
    packages        = []

    def layout (self):
        print ("Layout !!!!!!!!!!!!!!!!!!")
        projectPath  = os.getcwd ().replace ('/Conan','')
        print (projectPath)

        self.folders.root = ".."
        self.folders.source = "."
        self.folders.build = "Build"

        cmake_layout (self, src_folder = projectPath, build_folder = projectPath + '/Build/Release')
        #cmake_layout (self)

    def source (self):
        print ("Source !!!!!!!!!!!")
        cmake_file = load (self, "CMakeLists.txt")
        #conanPackages.install (self, self.repoPath, self.repoUrl, self.packages)

    def build (self):
        print ("Build !!!!!!!!!!!!!!!!!!")
        print (os.getcwd ())
        projectPath  = os.getcwd ().replace ('/Build/Release','')
        buildPath = projectPath

        if self.settings.os == 'Linux' and self.settings.compiler == 'gcc':
            #packagePaths = conanPackages.getPaths (self, self.packagePath, self.packages)
            cmake        = CMake (self)
            '''
            conanPath = self.folders.root + '/Conan/' + "/PackagesProperties.txt"

            print ("Conan path !!!!!")
            print (conanPath)
            packagesPropertiesFileHandler = open (conanPath, "w")
            for packagePathKey, packagePathValue in packagePaths.items ():
                packagesPropertiesFileHandler.writelines (packagePathKey + "=" + packagePathValue + "\n")
            packagesPropertiesFileHandler.close ()
            '''
            cmake.configure ()
            cmake.build     ()
        else:
            raise Exception ('Unsupported platform or compiler')

    def package (self):
        packagePath = self.packagePath + '/' + self.name

        copy (self, '*.h'  , src = os.path.join (self.source_folder, "Project"), dst = os.path.join (packagePath, "include"), keep_path = False)
        copy (self, '*.hxx', src = os.path.join (self.source_folder, "Project"), dst = os.path.join (packagePath, "include"), keep_path = False)
        copy (self, '*.a'  , src = self.build_folder                           , dst = os.path.join (packagePath, "lib")    , keep_path = False)

        copy (self, "*.h"  , self.build_folder, os.path.join (self.package_folder, "include"), keep_path = False)
        copy (self, "*.lib", self.build_folder, os.path.join (self.package_folder, "lib")    , keep_path = False)
        copy (self, "*.a"  , self.build_folder, os.path.join (self.package_folder, "lib")    , keep_path = False)

    def export_sources (self):
        print ("Export sources !!!!!!!!!!!")

        # The path of the CMakeLists.txt and sources we want to export are one level above
        folder = os.path.join (self.recipe_folder, "..")
        copy (self, "*.txt"        , folder, self.export_sources_folder)
        copy (self, "Tests/*.hxx"  , folder, self.export_sources_folder)
        copy (self, "Tests/*.cxx"  , folder, self.export_sources_folder)
        copy (self, "Project/*.h"  , folder, self.export_sources_folder)
        copy (self, "Project/*.cpp", folder, self.export_sources_folder)