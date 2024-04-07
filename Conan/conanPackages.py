import os, re
from   conan.tools.scm   import Git
from   conan.tools.files import replace_in_file

class conanPackages:
    def __createFolderDownload (self, vRepoPath):
        print ('createFolderDownload')
        if not os.path.isdir (vRepoPath):
            os.mkdir (vRepoPath)
        os.chdir (vRepoPath)

    def __cloneRepo (self, vName, vVersion, vRepoPath, vRepoUrl):
        print ('cloneRepo')
        repoUrl = vRepoUrl + '/' + vName + '.git'
        print ('url', repoUrl)

        packageDownloadPath = vRepoPath + '/' + vName
        print (packageDownloadPath)
        if not os.path.isdir (packageDownloadPath):
            git = Git (self)
            git.clone    (url = repoUrl, target = vName)
            git.folder = vName 
            git.checkout (commit = 'tags/' + vVersion)

        os.chdir (packageDownloadPath + '/Conan')

    def __createPackage (self, vUser, vChannel):
        print ('createPackage')
        self.run ('conan create . --user ' + vUser + ' --channel ' + vChannel)
        
    def __parse (self, vPackage):
        packageComponent = (re.split('[/@]', vPackage, 3))
        return {'name' : packageComponent [0], 'version' : packageComponent [1], 'user' : packageComponent [2], 'channel' : packageComponent [3]}

    def getPaths (self, vPackagePath, vPackages):
        print ('getPaths')
        paths        = {}
        packageNames = []
        for package in vPackages:
            print ("parse: ", package)
            packageComponent   = conanPackages.__parse (self, package)
            path               = vPackagePath + '/' + packageComponent ['name'] + '/' + packageComponent ['version'] + '/' + packageComponent ['user'] + '/' + packageComponent ['channel'] + '/package'
            hashFolder         = os.listdir (path)
            packageIncludePath = path + '/' + hashFolder [0] + '/include'
            packageLibPath     = path + '/' + hashFolder [0] + '/lib'
            packageName        = 'lib' + packageComponent ['name'] + 'Lib.a'
             
            if not os.path.isdir (packageIncludePath):
                raise Exception ('%s. Is not package include path', packageIncludePath)

            if not os.path.isdir (packageLibPath):
                raise Exception ('%s. Is not package include lib path', packageLibPath)

            paths [packageComponent ['name'] + 'PackageIncludePath'] = packageIncludePath
            paths [packageComponent ['name'] + 'PackageLibPath']     = packageLibPath
            paths [packageComponent ['name'] + 'PackageName']        = packageName
            packageNames.append (packageComponent ['name'])

        print (str (packageNames).strip ('[]').replace (',','').replace ('\'', ''))
        replace_in_file (self, self.folders.root + "/CMakeLists.txt", "PackagesTempNames", str (packageNames).strip ('[]').replace (',','').replace ('\'', ''), False)
        return paths

    def install (self, vRepoPath, vRepoUrl, vPackages):
        print ('install')
        for package in vPackages:
            packageComponent = conanPackages.__parse (self, package)
            conanPackages.__createFolderDownload     (self, vRepoPath)
            conanPackages.__cloneRepo                (self, packageComponent ['name'], packageComponent ['version'], vRepoPath, vRepoUrl)
            conanPackages.__createPackage            (self, packageComponent ['user'], packageComponent ['channel'])
