import json,urllib
import pprint
import sys
sys.path.append("../konfigFiles")
import krKonfig

# -*- coding: utf-8 -*-



def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')



strAPIKey = krKonfig.getApiKey()
strUserInfoURL = "https://www.wanikani.com/api/user/" + strAPIKey + "/user-information"
strLevelBaseURL = "https://www.wanikani.com/api/user/" + strAPIKey + "/kanji/"
strReport = ""
strEndl = "\n"

a_strReportInfoMatrix = []

a_strKDKanjiList = krKonfig.getKanjiList()

a_strKDKanjiConvList = []
a_strWKKanjiList = []
a_strIntersect = []
a_strDistinct = []

for v in range(0, len(a_strKDKanjiList)):
    a_strKDKanjiConvList.append(safe_str( unicode(a_strKDKanjiList[v],'utf-8')))

#f = open('KD-KANJI-LIST.txt')
#a_strKDKanjiList = f.readlines()
#a_strKDKanjiList = [line.strip() for line in open('KD-KANJI-LIST.txt')]
#f.close()


#with open("KD-KANJI-LIST.txt", "r") as f:
#  for line in f:
#    c = line.strip()
#    a_strKDKanjiList.append(c)


response = urllib.urlopen(strUserInfoURL)
data = json.loads(response.read())
strReport += "Current Level: " + str(data['user_information']['level']) + strEndl

for i in range(1, data['user_information']['level']+1):
    a_strCurrentLevelInfo = {}
    a_strCurrentLevelInfo["level"] = i
    currentLevelInfoJson = urllib.urlopen(strLevelBaseURL + str(i))
    strCurrentLevelData = json.loads(currentLevelInfoJson.read())
    a_strCurrentLevelInfo['availableKanji'] = len(strCurrentLevelData['requested_information'])
    a_strCurrentLevelInfo['unlockedKanjiCount'] = 0
    a_strCurrentLevelInfo['unlockedKanji'] = []
    for n in range(0, len(strCurrentLevelData['requested_information'])):
        if strCurrentLevelData['requested_information'][n]['user_specific'] != None:
            a_strCurrentLevelInfo['unlockedKanjiCount'] += 1
            a_strCurrentLevelInfo['unlockedKanji'].append(strCurrentLevelData['requested_information'][n]["character"])
            a_strWKKanjiList.append(strCurrentLevelData['requested_information'][n]["character"])

    a_strReportInfoMatrix.append(a_strCurrentLevelInfo)

for y in range(0, len(a_strWKKanjiList)):
    if safe_str(a_strWKKanjiList[y]) in a_strKDKanjiConvList:
        a_strIntersect.append(a_strWKKanjiList[y])
    else:
        a_strDistinct.append(a_strWKKanjiList[y])

bDoReport = True

#print safe_str( unicode(a_strKDKanjiList[5],'utf-8'))
#print safe_str(a_strWKKanjiList[7])
#for k in range(0, len(a_strKDKanjiList)):
#    try:
#        KDconv = unicode(a_strKDKanjiList[k],'utf-8')
#        print "- " + safe_str(KDconv)
#    except:
#        print "* " + a_strKDKanjiList[k]
    
#print safe_str(a_strWKKanjiList[7])
#print safe_str(KDconv) == safe_str(a_strWKKanjiList[7])
#print type(safe_unicode(a_strKDKanjiList[0]))
if bDoReport:
    iTotalKanji = 0
    print "Current Level: " + str(len(a_strReportInfoMatrix)) 
    for x in range(0, len(a_strReportInfoMatrix)):
        print "Level " + str(x+1) + ": Kanji " + str(a_strReportInfoMatrix[x]['unlockedKanjiCount']) + "/" + str(a_strReportInfoMatrix[x]['availableKanji'])
        iTotalKanji += a_strReportInfoMatrix[x]['unlockedKanjiCount']
        print ", ".join(a_strReportInfoMatrix[x]['unlockedKanji']) + strEndl

    #print "Total WK Kanji: " + str(iTotalKanji)
    #print "Total KD Kanji: " +str(len(a_strKDKanjiList))
    print "Total Kanji: " + str(len(a_strDistinct) + len(a_strKDKanjiList)) + strEndl
    print "All KD Kanji: ("+ str(len(a_strKDKanjiList)) +")"
    print ",".join(a_strKDKanjiList)
    print "--------------------------------------"
    print "All WK Kanji: ("+ str(iTotalKanji) +")"
    print ",".join(a_strWKKanjiList)
    print "--------------------------------------"
    print "INTERSECT: " + str(len(a_strIntersect))
    print ",".join(a_strIntersect)
    print "--------------------------------------"
    print "DISTINCT: " + str(len(a_strDistinct))
    print ",".join(a_strDistinct)


    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(a_strReportInfoMatrix)
    #print strReport
    #strChoice = raw_input("> ")
