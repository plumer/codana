from projectdata import DataManager

class PredictDataBuilder:
    def __init__(self, version):
        self.dataManage = DataManager(version)

    def buildCsv(self, csvPath):
        csvFile = open(csvPath, 'w')
        filelist = self.dataManage.getFilenames()
        attrlist = self.dataManage.listFileAttr()
        for filename in filelist:
            csvFile.write(filename + ',')
            attrs = self.dataManage.getFileAttr(filename)
            for attr in attrlist:
                csvFile.write(attrs[attr] + ',')
            bugnum = self.dataManage.getBugNumberOfFile(filename)
            csvFile.write(str(bugnum) + ',')
            if bugnum == 0:
                csvFile.write('0\n')
            else:
                csvFile.write('1\n')
        csvFile.close()

if __name__ == '__main__':
    PredictDataBuilder('8.0.21').buildCsv('predict.csv')

