import urllib
import urllib2
import cookielib
import re

#bugurl = r"https://bugzilla.kernel.org/show_bug.cgi?id=%d"
#fixedurl = r'https://bugzilla.kernel.org/show_activity.cgi?id=%d'
bugurl = r'https://bz.apache.org/bugzilla/show_bug.cgi?id=%d'
fixedurl = r'https://bz.apache.org/bugzilla/show_activity.cgi?id=%d'

titlepa = re.compile(r"(?<=hideAliasAndSummary\(').*?(?=',)", re.S)
statuspa = re.compile(r'(?<="static_bug_status">).*?(?=<)', re.S)
productpa = re.compile(r'(?<="field_container_product" >).*?(?=<)', re.S)
componentpa = re.compile(r'(?<="field_container_component" >).*?(?=<)', re.S)
hardwarepa = re.compile(r'Hardware.*?</a>[\s\n]*</label>[\s\n]*</th>[\s\n]*<td class="field_value">.*?<', re.S)
importancepa = re.compile(r'mportance</a></label>:[\s\n]*</th>[\s\n]*<td>.*?<', re.S)
versionpa = re.compile(r'Version:</a>[\s\n]*</label>[\s\n]*</th>[\s\n]*<td>.*?<', re.S)
reportpa = re.compile(r'Reported:[\s\n]*</th>[\s\n]*<td>.*?<.*?<.*?</', re.S)
fixedpa = re.compile(r'(?<=<table border cellpadding="4">).*?(?=</table>)', re.S)
subcellpa = re.compile(r'(?<=>)\w+.*?(?=<)', re.S)

logfile = open('result/log.txt', 'w')

for bugnum in xrange(135, 1000):
    print 'Bug #' + str(bugnum) + ':'
    print '> opening url...'
    bugweb = urllib.urlopen(bugurl % bugnum).read()
    fixedweb = urllib.urlopen(fixedurl % bugnum).read()
    print '> building report...'
    results = titlepa.findall(bugweb)
    if len(results) == 0:
        print 'Permission Denied.'
        logfile.write('Bug #%d: Permission Denied\n' % bugnum)
        continue
    bugfile = open('result/bug%d.txt' % bugnum, 'w')
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Bug #' + str(bugnum) + ': ' + result + '\n\n')
    results = statuspa.findall(bugweb)
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Status: ' + result + '\n')
    results = productpa.findall(bugweb)
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Product: ' + result + '\n')
    results = componentpa.findall(bugweb)
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Component: ' + result + '\n')
    results = hardwarepa.findall(bugweb)
    results = subcellpa.findall(results[0])
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Hardware: ' + result + '\n')
    results = importancepa.findall(bugweb)
    results = subcellpa.findall(results[0])
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Importance: ' + result + '\n')
    results = versionpa.findall(bugweb)
    results = subcellpa.findall(results[0])
    if len(results) != 0:
        result, count = re.subn(r'&nbsp', r' ', results[0])
        result, count = re.subn(r'[\s\n]+', r' ', results[0])
    else:
        result = ''
    bugfile.write('Version: ' + result + '\n')
    results = reportpa.findall(bugweb)
    results = subcellpa.findall(results[0])
    result, count = re.subn(r'&nbsp', r' ', results[0])
    result, count = re.subn(r'[\s\n]+', r' ', results[0])
    bugfile.write('Reported: ' + result)
    result, count = re.subn(r'&nbsp', r' ', results[1])
    result, count = re.subn(r'[\s\n]+', r' ', results[1])
    bugfile.write(result + '\n')
    
    results = fixedpa.findall(fixedweb)
    bugfile.write('\n\n' + results[0] + '\n')
    print '> Done!'
    bugfile.close()

logfile.close()
