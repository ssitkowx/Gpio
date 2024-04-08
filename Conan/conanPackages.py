import os, re
from   conan.tools.scm import Git

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
    
    def install (self, vRepoPath, vRepoUrl, vPackages):
        print ('install')
        for package in vPackages:
            packageComponent = conanPackages.__parse (self, package)
            conanPackages.__createFolderDownload     (self, vRepoPath)
            conanPackages.__cloneRepo                (self, packageComponent ['name'], packageComponent ['version'], vRepoPath, vRepoUrl)
            conanPackages.__createPackage            (self, packageComponent ['user'], packageComponent ['channel'])
