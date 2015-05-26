from projectdata import DataManager

class PredictDataBuilder:
    def __init__(self, version):
        self.dataManage = DataManager().getManager(version)

    def buildCsv(self, csvPath):
        csvFile = open(csvPath, 'w')
        filelist = self.dataManage.getFilenames()
        attrlist = self.dataManage.listFileAttr()
        for filename in filelist:
            csvFile.write(str(hash(filename)) + ',')
            attrs = self.dataManage.getFileAttr(filename)
            for attr in attrlist:
                csvFile.write(attrs[attr] + ',')
            bugnum = self.dataManage.getBugNumberOfFile(filename)
            if bugnum == 0:
                csvFile.write('NoBug\n')
            else:
                csvFile.write('Buggy\n')
        csvFile.close()

class PredictTestBuilder:
    def __init__(self, version):
        self.filename = []
        self.fileattr = []
        testFile = open(r'tomcat_history/tomcat' + version + '/tomcat_pack.txt', 'r')
        for packs in testFile:
            packslice = packs.strip(' \t\n').split('\t')
            filenum = 0
            if int(packslice[1]) == 0:
                continue
            for files in testFile:
                fileslice = files.strip(' \t\n').split('\t')
                if not fileslice[0] in self.filename:
                    self.filename.append(fileslice[0])
                    self.fileattr.append([str(hash(fileslice[0]))] + fileslice[1:])
                filenum = filenum + 1
                if filenum >= int(packslice[1]):
                    break
        testFile.close()

    def buildCsv(self, csvPath):
        csvFile = open(csvPath, 'w')
        for files in self.fileattr:
            for attrs in files:
                csvFile.write(attrs + ',')
            csvFile.write('NoBug\n')
        csvFile.close()

if __name__ == '__main__':
    PredictDataBuilder('8.0.21').buildCsv('predict.csv')
    PredictTestBuilder('8.0.23').buildCsv('predicttest.csv')

