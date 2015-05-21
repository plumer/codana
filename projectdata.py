class DataManager:
    """Manager of all the information of files and packages

    Attributes:
        packages (list of str): List of packages name
        files (list of str): List of all the files in the project
        packagedict (dict): Map of packages(key) and filename(value)
        fileattr (dict): Map of filename(key) and the attributes of the file(value)
        packageattr (dict): Map of package(key) and the attributes of the package(value)
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
            self.packageattr[packslice[0]] = self.packPackageAttr(packslice[2:])
            filenum = 0
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

    def packPackageAttr(self, attrs):
        return {'filenum' : attrs[0],
                'classnum' : attrs[1],
                'codelines' : attrs[2]}

    def packFileAttr(self, attrs):
        return {'codelines' : attrs[0],
                'classnum' : attrs[1],
                'localmethodsnum' : attrs[2],
                'classmethodsnum' : attrs[3]}

    def getPackages(self):
        return self.packages

    def getFilenames(self):
        return self.files

    def getFilesOfPackage(self, package):
        return self.packagedict[package]

    def getFileAttr(self, filename):
        return self.fileattr[filename]

    def getPackageAttr(self, package):
        return self.packageattr[package]

if __name__ == '__main__':
    DataManager()
