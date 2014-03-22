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

a_strKDKanjiList = ["一","二","三","了","子","女","好","姦","口","品","言","下","不","否","十","古","叶","計","匕","七","比","叱","日","旨","昆","唱","晶","旧","早","旦","白","皆","水","泉","氷","永","泳","泊","汁","混","月","湖","明","脂","胆","朝","火","炎","淡","談","丁","灯","可","河","訂","田","町","畑","胃","入","人","何","信","化","花","苦","草","荷","冂","内","肉","円","市","肺","姉","目","冒","帽","自","亠","亭","停","卒","万","方","訪","妨","肪","又","双","奴","文","斉","済","丩","収","叫","心","必","怒","息","思","兦","亡","忙","忘","盲","妄","罒","曼","慢","漫","亜","悪","夕","多","夢","夜","液","名","歹","死","卜","外","上","卓","占","点","宀","宅","安","字","宣","喧","八","穴","六","沿","厶","公","訟","台","治","始","怠","能","熊","態","仏","并","立","辛","幸","宰","泣","位","音","章","暗","意","億","憶","門","闇","間","問","刀","前","切","召","昭","分","剤","罰","刃","忍","認","力","加","協","脅","努","男","九","究","丸","享","孰","熟","執","小","少","劣","妙","省","京","涼","景","示","宗","叔","寂","督","幺","幼","玄","畜","蓄","糸","紹","線","帛","綿","細","総","索","納","紛","絹","系","孫","係","干","刊","用","肝","芋","汗","宇","千","舌","話","活","辞","憩","半","判","伴","平","評","呼","土","里","量","黒","童","憧","埋","坊","吐","塾","士","仕","志","吉","詰","結","誌","⺹","老","孝","者","著","緒","諸","署","暑","煮","隹","焦","無","維","唯","誰","準","護","馬","止","雌","肯","歩","渉","紫","足","促","踏","正","是","定","証","歪","走","超","尺","駅","昼","訳","沢","手","択","推","描","提","払","批","指","打","招","拐","担","接","拍","挿","看","耳","取","最","撮","趣","恥","聞","斤","折","丘","哲","誓","訴","竹","筋","簡","乍","作","昨","辶","近","辺"]
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
