import os, re
from   conan.tools.scm   import Git
from   conan.tools.files import replace_in_file

class conanPackages:
    def __parse (self, vPackage):
        packageComponent = (re.split('[/]', vPackage))
        return {'name' : packageComponent [0], 'version' : packageComponent [1] }
    
    def __createRepo (self, vRepoPath):
        print ('createRepoFolder')
        if not os.path.isdir (vRepoPath):
            os.mkdir (vRepoPath)
        os.chdir (vRepoPath)

    def __createPackage (self, vName, vVersion):
        print ('createPackage')
        self.run ('conan create . --name ' + vName + ' --version ' + vVersion)

    def __updateCMakeLists (self, vProjectPath, vSearch, vReplace):
        replace_in_file (self, os.path.join (vProjectPath, "CMakeLists.txt"), vSearch, vReplace, False)
    
    def __cloneRepo (self, vName, vVersion, vRepoPath, vRepoUrl):
        print ('cloneRepo')
        repoUrl = vRepoUrl + '/' + vName + '.git'
        print ('url', repoUrl)

        packagePath = vRepoPath + '/' + vName
        print (packagePath)
        if not os.path.isdir (packagePath):
            git = Git (self)
            git.clone    (url = repoUrl, target = vName)
            git.folder = vName 
            git.checkout (commit = 'tags/' + vVersion)

        os.chdir (packagePath + '/Conan')

    def install (self, vRepoPath, vRepoUrl, vPackages):
        print ('install')

        projectPath = os.getcwd ().replace ('/Build/Release','')
        conanPackages.__updateCMakeLists (self, projectPath, "SET (PackageIncludePath )", "SET (PackageIncludePath " + self.packagePath + ")")

        packageNames = []
        for package in vPackages:
            packageComponent = conanPackages.__parse (self, package)
            conanPackages.__createRepo               (self, vRepoPath)
            conanPackages.__cloneRepo                (self, packageComponent ['name'], packageComponent ['version'], vRepoPath, vRepoUrl)
            conanPackages.__createPackage            (self, packageComponent ['name'], packageComponent ['version'])

            packageNames.append (packageComponent ['name'])
        conanPackages.__updateCMakeLists (self, projectPath, "SET (PackageNames )", "SET (PackageNames " + " ".join (packageNames) + ")")