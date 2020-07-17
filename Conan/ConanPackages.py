import os, re, sys
from conans import tools

class ConanPackages:
    def __createFolderDownload (self, v_downloadsPath):
        print ('createFolderDownload')
        if not os.path.isdir (v_downloadsPath):
            os.mkdir (v_downloadsPath)
        os.chdir (v_downloadsPath)

    def __cloneRepo (self, v_name, v_downloadsPath, v_repoUrl):
        print ('cloneRepo')
        url = v_repoUrl + '/' + v_name + '.git'
        print ('url', url)

        packageDownloadsPath = v_downloadsPath + '/' + v_name
        if not os.path.isdir (packageDownloadsPath):
            self.run ('git clone ' + url)
        os.chdir (packageDownloadsPath + '/Conan')

    def __createPackage (self, v_user, v_channel):
        print ('createPackage')
        self.run('conan create . ' + v_user + '/' + v_channel)
        
    def __parse (self, v_package):
        packageComponent = (re.split('[/@]', v_package, 3))
        return {'name' : packageComponent [0], 'version' : packageComponent [1], 'user' : packageComponent [2], 'channel' : packageComponent [3]}

    def GetPaths (self, v_packagesPath, v_packages):
        print ('GetPaths')
        paths        = {}
        packageNames = []
        for package in v_packages:
            print ("parse: ", package)
            packageComponent   = ConanPackages.__parse (self, package)
            path               = v_packagesPath + '/' + packageComponent ['name'] + '/' + packageComponent ['version'] + '/' + packageComponent ['user'] + '/' + packageComponent ['channel'] + '/package'
            hashFolder         = os.listdir (path)
            packageIncludePath = path + '/' + hashFolder [0] + '/include'
            packageLibPath     = path + '/' + hashFolder [0] + '/lib'
            packageName        = packageComponent ['name'] + 'Lib.lib'
             
            if not os.path.isdir (packageIncludePath):
                raise Exception ('%s. Is not package include path', packageIncludePath)

            if not os.path.isdir (packageLibPath):
                raise Exception ('%s. Is not package include lib path', packageLibPath)

            paths [packageComponent ['name'] + 'PackageIncludePath'] = packageIncludePath
            paths [packageComponent ['name'] + 'PackageLibPath']     = packageLibPath
            paths [packageComponent ['name'] + 'PackageName']        = packageName
            packageNames.append (packageComponent ['name'])

        tools.replace_in_file (os.getcwd ().replace ('\Conan','') + "\\CMakeLists.txt", "PackagesTempNames", str (packageNames).strip ('[]').replace (',','').replace ('\'', ''), False)    
        return paths

    def Install (self, v_downloadsPath, v_repoUrl, v_packages):
        print ('Install')
        for package in v_packages:
            packageComponent = ConanPackages.__parse (self, package)
            ConanPackages.__createFolderDownload     (self, v_downloadsPath)
            ConanPackages.__cloneRepo                (self, packageComponent ['name'], v_downloadsPath, v_repoUrl)
            ConanPackages.__createPackage            (self, packageComponent ['user'], packageComponent ['channel'])
