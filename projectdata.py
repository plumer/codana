class DataManager:
    """Manager of all the information of files and packages

    Attributes:
        packages (list of str): List of packages name
        files (list of str): List of all the files in the project
        packagedict (dict): Map of packages(key) and filenames(value)
        filebugnum (dict): Map of filename(key) and bug numbers(value)
        fileattr (dict): Map of filename(key) and the attributes of the file(value)
        packageattr (dict): Map of package(key) and the attributes of the package(value)
    """
    def __init__(self, version='6.0.0'):
        self.packagedict = {}
        self.fileattr = {}
        self.files = []
        self.filebugnum = {}
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
        datafile.close()
        datafile = open(r'tomcat_history/tomcat' + version + r'/log.txt', 'r')
        for record in datafile:
            recordslice = record.strip(' \t\n').split('\t')
            self.filebugnum[recordslice[0]] = int(recordslice[1])
        datafile.close()
        self.packages = self.packagedict.keys()

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
        return self.packages

    def getFilenames(self):
        return self.files

    def getFilesOfPackage(self, package):
        return self.packagedict[package]

    def getPackageOfFile(self, filename):
        return self.filedict[filename]

    def getFileAttr(self, filename):
        return self.fileattr[filename]

    def getPackageAttr(self, package):
        return self.packageattr[package]

    def getBugNumberOfFile(self, filename):
        return self.filebugnum[filename]

    def getBugNumberOfPackage(self, package):
        bugnum = 0
        for filename in self.packagedict[package]:
            bugnum = bugnum + self.filebugnum[filename]
        return bugnum

if __name__ == '__main__':
    DataManager()
