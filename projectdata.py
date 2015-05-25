class DataManager:
    """Manager of all the information of files and packages

    Attributes:
        packages (list of str): List of packages name
        files (list of str): List of all the files in the project

        packagedict (dict): Map of packages(key) and filename(value)

        fileattr (dict): Map of filename(key) and the attributes of the file(value)
        packageattr (dict): Map of package(key) and the attributes of the package(value)

        filedepends (list of tuple): List of all the edges in the dependence graph of all files
        packagedepends (list of tuple) : List of all the edges in the dependence graph of all packages
    """
    def __init__(self, version='6.0.0'):
        self.packagedict = {}
        self.fileattr = {}
        self.files = []
        self.packageattr = {}
        datafile = open(r'tomcat_history/tomcat' + version + r'/tomcat_pack.txt', 'r')
        for packs in datafile:
            packslice = packs.strip(' \t\n').split('\t')
            self.packagedict[packslice[0]] = []
            self.packageattr[packslice[0]] = self.packPackageAttr(packslice[1:])
            filenum = 0
            if int(packslice[1]) == 0:
                continue
            for files in datafile:
                fileattr = files.strip(' \t\n').split('\t')
                if not fileattr[0] in self.packagedict[packslice[0]]:
                    self.files.append(fileattr[0])
                    self.packagedict[packslice[0]].append(fileattr[0])
                    self.fileattr[fileattr[0]] = self.packFileAttr(fileattr[1:])
                filenum = filenum + 1
                if filenum >= int(packslice[1]):
                    break
        self.packages = self.packagedict.keys()

        self.packagedepends = []
        packdependfile = open(r'tomcat_history/tomcat' + version + r'/tomcat_pack_depends.txt', 'r')
        for e in packdependfile:
            vertices = e.strip(' \t\n').split(' ')
            self.packagedepends.append( (vertices[0], vertices[-1]) )
        packdependfile.close()

        self.filedepends = []
        filedependfile = open(r'tomcat_history/tomcat' + version + r'/tomcat_depends.txt', 'r')
        for e in filedependfile:
            vertices = e.strip(' \t\n').split(' ')
            self.filedepends.append( (vertices[0], vertices[-1]) )
        filedependfile.close()

    def packPackageAttr(self, attrs):
        return {'filenum' : attrs[0],
                'codelines' : attrs[1],
                'cyclomatic' : attrs[2]}

    def packFileAttr(self, attrs):
        return {'codelines' : attrs[0],
                'cyclomatic' : attrs[1]}

    def listFileAttr(self):
        return ('codelines', 'cyclomatic')

    def listPackageAttr(self):
        return ('filenum', 'codelines' , 'cyclomatic')

    def getPackages(self):
        return self.packages[:]

    def getFilenames(self):
        return self.files[:]

    def getFilesOfPackage(self, package):
        return self.packagedict[package][:]

    def getFileAttr(self, filename):
        return self.fileattr[filename].copy()

    def getPackageAttr(self, package):
        if self.packageattr.has_key(package):
            return self.packageattr[package].copy()
        else:
            return None

    def getFileDependence(self):
        return self.filedepends

    def getPackageDependence(self):
        return self.packagedepends

if __name__ == '__main__':
    DataManager()
