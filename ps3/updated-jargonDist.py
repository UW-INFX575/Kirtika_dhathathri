import math
import os
import csv
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.stem.wordnet import WordNetLemmatizer
import time

# abstractFile = "abstracts.txt"
# groupIdFile = "groups.txt"

abstractFile = "abstracts2.txt"
groupIdFile = "groups2.txt"

stopListFile = "stopwords.txt"
osPathFile = "allfiles"
    
def createFiles():    
    ### creating file anf grouping them
    f1 = open(abstractFile,'r')
    f1.readline()# skip first line
    count = 0
    for line in f1:
        print 'entered abstract...'
        #print line
        #print '-----'
        count = count + 1    
        content = line.split('\t')
       
        var = '0'
        f2 = open(groupIdFile,'r')
        f2.readline()# skip first line
        for line in f2:
            #print 'entered groupfile...'
            line = line.split('\t')
            print 'groupFile- : ' + line[0]
            print 'abstractFile- : ' + content[0]
            if( line[0] == content[0] ):
                var = line[1].split()[0].strip()
                print 'group_' + var
                break
        
        filename = 'file'+ '_group' + str(var) + '_' + str(count) +'.csv'
        #print filename
        #f = csv.writer(open(filename,'wb'))
        f3 = csv.writer(open(os.path.join(osPathFile, filename), "wb"))
        #print content[1]
        if (re.match('null',content[1].strip())):
            #print 'yes'            
            print filename
        else:
            f3.writerow([content[1]])
            #print 'no'
        #print '----'
    
    #print 'number of files ' + str(count)
    print "Done creating files"


'''
create the stop-word list
'''
def stoplist():
    f1 = open(stopListFile,'r')
    for line in f1:
        stopList = re.findall('"([^"]*)"', line)
        
    #print stopList
    return stopList
    
def createWordList(group,stopList):    
    folder =  os.listdir(osPathFile) 
    #print folder
    tokens = RegexpTokenizer(r'\w+')
    
    wordList = []
    stops = set(stopList)
    #print stops
    
    for files in folder:
        if ( re.search(group,files) ):            
            fp = open(os.path.join(osPathFile, files), "r")
            #print files
            line = fp.read()
            #print line
            line = tokens.tokenize(line)
            for w in line:        
                if w.lower() not in stops:
                    #print w
                    wordList.append(w)
            
    #print wordList
    #print len(wordList)
    return wordList

def createUniqueWordList(wordlist):    
    uniqueWords = [] 
    for i in wordlist:
        if not i in uniqueWords:
            uniqueWords.append(i);
            
    return uniqueWords

'''
function to calculate probability distribution of various files
'''
def createProbDist(readerWordlist,writerUniqueWordlist):      
        
    ### create a dictionary to store the frequency of each term
    prob_dist = []
    
    ### using nltk calcuate frequency of each word
    unigramWordList = FreqDist(readerWordlist)
    datalen = len(readerWordlist) ### total words in the that document
    #print len(unigramWordList)
    #print datalen
    
    for word in writerUniqueWordlist:
        if word in unigramWordList:
            #print word
            #print unigramWordList.get(word)
            #print unigramWordList.get(word)/float(datalen)
            prob_dist.append(unigramWordList.get(word)/float(datalen))
        else:
            prob_dist.append(0)
            
    #print prob_dist
    return prob_dist

def createPDwithTeleport(readerWordlist,mergedWordList):
    ### teleporation paramerter with value of 1 percent 
    
    corpusPD = {}
    readerPD = {}
    
    unigramReaderWordList = FreqDist(readerWordlist)
    unigramCorpusWordList = FreqDist(mergedWordList)
    
    for word in unigramCorpusWordList.keys():
        
        corpusPD[word] = unigramCorpusWordList[word]/float(sum(unigramCorpusWordList.values()))
        
        if word in unigramReaderWordList:
            readerPD[word] = unigramReaderWordList[word]/float(sum(unigramReaderWordList.values()))
        else:
            readerPD[word] = 0
            
        readerPD[word] = 0.99*readerPD[word] + 0.01*corpusPD[word]
        
    return readerPD
    
def shannonEntropy(px):
        H_x = 0
        for p in px.values():
            try:
                H_x += - p * math.log(p, 2)
            except:
                H_x += 0
        #print H_x
        return H_x

### calculate KL divergence from p_xs -> p_ys
def klDivergence(p_xs,p_ys):
    
    Q_xy = 0
    
    for word in p_xs.keys():
        try:
            Q_xy += - p_xs[word] * math.log(p_ys[word], 2)
        except:
            Q_xy += 0
            
    #print Q_xy
    return Q_xy
                 
def calcCulturalHole(pdx,pdy):
    
    #Shannon entrotpy of pdx
    H_pdx = shannonEntropy(pdx)
    Q_xy = klDivergence(pdx,pdy)    
    
    ### cultural hole
    E_xy = H_pdx/Q_xy
    #print E_xy
    C_xy = 1 - E_xy
    
    #print ('Cultural hole: %f' % C_xy)
    return C_xy



### driver function
start_time = time.time()
createFiles()
stops = stoplist()

### create wordlists
group1_WordList = createWordList('group1',stops)
group2_WordList = createWordList('group2',stops)
group3_WordList = createWordList('group3',stops)
group4_WordList = createWordList('group4',stops)
group5_WordList = createWordList('group5',stops)
group6_WordList = createWordList('group6',stops)
group7_WordList = createWordList('group7',stops)
group8_WordList = createWordList('group8',stops)
group9_WordList = createWordList('group9',stops)
group10_WordList = createWordList('group10',stops)
mergedWordList = group1_WordList+group2_WordList+group3_WordList+group4_WordList+group5_WordList+group6_WordList+group7_WordList+group8_WordList+group9_WordList+group10_WordList 
#print group1_WordList
#print len(group1_WordList)
#print group2_WordList
#print len(group2_WordList)
#print group3_WordList
#print len(group3_WordList)
#print mergedWordList
#print len(mergedWordList)

# ### calc probablity distrbution
group1_pd = createPDwithTeleport(group1_WordList,mergedWordList)
group2_pd = createPDwithTeleport(group2_WordList,mergedWordList)
group3_pd = createPDwithTeleport(group3_WordList,mergedWordList)
group4_pd = createPDwithTeleport(group4_WordList,mergedWordList)
group5_pd = createPDwithTeleport(group5_WordList,mergedWordList)
group6_pd = createPDwithTeleport(group6_WordList,mergedWordList)
group7_pd = createPDwithTeleport(group7_WordList,mergedWordList)
group8_pd = createPDwithTeleport(group8_WordList,mergedWordList)
group9_pd = createPDwithTeleport(group9_WordList,mergedWordList)
group10_pd = createPDwithTeleport(group10_WordList,mergedWordList)


print 'started calculating cultural holes...'

ch_11 = calcCulturalHole(group1_pd,group1_pd)
ch_12 = calcCulturalHole(group1_pd,group2_pd)
ch_13 = calcCulturalHole(group1_pd,group3_pd)
ch_14 = calcCulturalHole(group1_pd,group4_pd)
ch_15 = calcCulturalHole(group1_pd,group5_pd)
ch_16 = calcCulturalHole(group1_pd,group6_pd)
ch_17 = calcCulturalHole(group1_pd,group7_pd)
ch_18 = calcCulturalHole(group1_pd,group8_pd)
ch_19 = calcCulturalHole(group1_pd,group9_pd)
ch_110 = calcCulturalHole(group1_pd,group10_pd)
print 'Done cultural hole 1->'

ch_21 = calcCulturalHole(group2_pd,group1_pd)
ch_22 = calcCulturalHole(group2_pd,group2_pd)
ch_23 = calcCulturalHole(group2_pd,group3_pd)
ch_24 = calcCulturalHole(group2_pd,group4_pd)
ch_25 = calcCulturalHole(group2_pd,group5_pd)
ch_26 = calcCulturalHole(group2_pd,group6_pd)
ch_27 = calcCulturalHole(group2_pd,group7_pd)
ch_28 = calcCulturalHole(group2_pd,group8_pd)
ch_29 = calcCulturalHole(group2_pd,group9_pd)
ch_210 = calcCulturalHole(group2_pd,group10_pd)
print 'Done cultural hole 2->'

ch_31 = calcCulturalHole(group3_pd,group1_pd)
ch_32 = calcCulturalHole(group3_pd,group2_pd)
ch_33 = calcCulturalHole(group3_pd,group3_pd)
ch_34 = calcCulturalHole(group3_pd,group4_pd)
ch_35 = calcCulturalHole(group3_pd,group5_pd)
ch_36 = calcCulturalHole(group3_pd,group6_pd)
ch_37 = calcCulturalHole(group3_pd,group7_pd)
ch_38 = calcCulturalHole(group3_pd,group8_pd)
ch_39 = calcCulturalHole(group3_pd,group9_pd)
ch_310 = calcCulturalHole(group3_pd,group10_pd)
print 'Done cultural hole 3->'

ch_41 = calcCulturalHole(group4_pd,group1_pd)
ch_42 = calcCulturalHole(group4_pd,group2_pd)
ch_43 = calcCulturalHole(group4_pd,group3_pd)
ch_44 = calcCulturalHole(group4_pd,group4_pd)
ch_45 = calcCulturalHole(group4_pd,group5_pd)
ch_46 = calcCulturalHole(group4_pd,group6_pd)
ch_47 = calcCulturalHole(group4_pd,group7_pd)
ch_48 = calcCulturalHole(group4_pd,group8_pd)
ch_49 = calcCulturalHole(group4_pd,group9_pd)
ch_410 = calcCulturalHole(group4_pd,group10_pd)
print 'Done cultural hole 4->'

ch_51 = calcCulturalHole(group5_pd,group1_pd)
ch_52 = calcCulturalHole(group5_pd,group2_pd)
ch_53 = calcCulturalHole(group5_pd,group3_pd)
ch_54 = calcCulturalHole(group5_pd,group4_pd)
ch_55 = calcCulturalHole(group5_pd,group5_pd)
ch_56 = calcCulturalHole(group5_pd,group6_pd)
ch_57 = calcCulturalHole(group5_pd,group7_pd)
ch_58 = calcCulturalHole(group5_pd,group8_pd)
ch_59 = calcCulturalHole(group5_pd,group9_pd)
ch_510 = calcCulturalHole(group5_pd,group10_pd)
print 'Done cultural hole 5->'

ch_61 = calcCulturalHole(group6_pd,group1_pd)
ch_62 = calcCulturalHole(group6_pd,group2_pd)
ch_63 = calcCulturalHole(group6_pd,group3_pd)
ch_64 = calcCulturalHole(group6_pd,group4_pd)
ch_65 = calcCulturalHole(group6_pd,group5_pd)
ch_66 = calcCulturalHole(group6_pd,group6_pd)
ch_67 = calcCulturalHole(group6_pd,group7_pd)
ch_68 = calcCulturalHole(group6_pd,group8_pd)
ch_69 = calcCulturalHole(group6_pd,group9_pd)
ch_610 = calcCulturalHole(group6_pd,group10_pd)
print 'Done cultural hole 6->'

ch_71 = calcCulturalHole(group7_pd,group1_pd)
ch_72 = calcCulturalHole(group7_pd,group2_pd)
ch_73 = calcCulturalHole(group7_pd,group3_pd)
ch_74 = calcCulturalHole(group7_pd,group4_pd)
ch_75 = calcCulturalHole(group7_pd,group5_pd)
ch_76 = calcCulturalHole(group7_pd,group6_pd)
ch_77 = calcCulturalHole(group7_pd,group7_pd)
ch_78 = calcCulturalHole(group7_pd,group8_pd)
ch_79 = calcCulturalHole(group7_pd,group9_pd)
ch_710 = calcCulturalHole(group7_pd,group10_pd)
print 'Done cultural hole 7->'


ch_81 = calcCulturalHole(group8_pd,group1_pd)
ch_82 = calcCulturalHole(group8_pd,group2_pd)
ch_83 = calcCulturalHole(group8_pd,group3_pd)
ch_84 = calcCulturalHole(group8_pd,group4_pd)
ch_85 = calcCulturalHole(group8_pd,group5_pd)
ch_86 = calcCulturalHole(group8_pd,group6_pd)
ch_87 = calcCulturalHole(group8_pd,group7_pd)
ch_88 = calcCulturalHole(group8_pd,group8_pd)
ch_89 = calcCulturalHole(group8_pd,group9_pd)
ch_810 = calcCulturalHole(group8_pd,group10_pd)
print 'Done cultural hole 8->'

ch_91 = calcCulturalHole(group9_pd,group1_pd)
ch_92 = calcCulturalHole(group9_pd,group2_pd)
ch_93 = calcCulturalHole(group9_pd,group3_pd)
ch_94 = calcCulturalHole(group9_pd,group4_pd)
ch_95 = calcCulturalHole(group9_pd,group5_pd)
ch_96 = calcCulturalHole(group9_pd,group6_pd)
ch_97 = calcCulturalHole(group9_pd,group7_pd)
ch_98 = calcCulturalHole(group9_pd,group8_pd)
ch_99 = calcCulturalHole(group9_pd,group9_pd)
ch_910 = calcCulturalHole(group9_pd,group10_pd)
print 'Done cultural hole 9->'

ch_101 = calcCulturalHole(group10_pd,group1_pd)
ch_102 = calcCulturalHole(group10_pd,group2_pd)
ch_103 = calcCulturalHole(group10_pd,group3_pd)
ch_104 = calcCulturalHole(group10_pd,group4_pd)
ch_105 = calcCulturalHole(group10_pd,group5_pd)
ch_106 = calcCulturalHole(group10_pd,group6_pd)
ch_107 = calcCulturalHole(group10_pd,group7_pd)
ch_108 = calcCulturalHole(group10_pd,group8_pd)
ch_109 = calcCulturalHole(group10_pd,group9_pd)
ch_1010 = calcCulturalHole(group10_pd,group10_pd)
print 'Done cultural hole 10->'

row = ['group 1', 'group 2', 'Cultural Hole']

outFile = csv.writer(open('crossEntropyResultsFor10Files.csv','wb'))
outFile.writerow(row)

row = ['1','1',ch_11]
outFile.writerow(row)
row = ['1','2',ch_12]
outFile.writerow(row)
row = ['1','3',ch_13]
outFile.writerow(row)
row = ['1','4',ch_14]
outFile.writerow(row)
row = ['1','5',ch_15]
outFile.writerow(row)
row = ['1','6',ch_16]
outFile.writerow(row)
row = ['1','7',ch_17]
outFile.writerow(row)
row = ['1','8',ch_18]
outFile.writerow(row)
row = ['1','9',ch_19]
outFile.writerow(row)
row = ['1','10',ch_110]
outFile.writerow(row)

row = ['2','1',ch_21]
outFile.writerow(row)
row = ['2','2',ch_22]
outFile.writerow(row)
row = ['2','3',ch_23]
outFile.writerow(row)
row = ['2','4',ch_24]
outFile.writerow(row)
row = ['2','5',ch_25]
outFile.writerow(row)
row = ['2','6',ch_26]
outFile.writerow(row)
row = ['2','7',ch_27]
outFile.writerow(row)
row = ['2','8',ch_28]
outFile.writerow(row)
row = ['2','9',ch_29]
outFile.writerow(row)
row = ['2','10',ch_210]
outFile.writerow(row)

row = ['3','1',ch_31]
outFile.writerow(row)
row = ['3','2',ch_32]
outFile.writerow(row)
row = ['3','3',ch_33]
outFile.writerow(row)
row = ['3','4',ch_34]
outFile.writerow(row)
row = ['3','5',ch_35]
outFile.writerow(row)
row = ['3','6',ch_36]
outFile.writerow(row)
row = ['3','7',ch_37]
outFile.writerow(row)
row = ['3','8',ch_38]
outFile.writerow(row)
row = ['3','9',ch_39]
outFile.writerow(row)
row = ['3','10',ch_310]
outFile.writerow(row)

row = ['4','1',ch_41]
outFile.writerow(row)
row = ['4','2',ch_42]
outFile.writerow(row)
row = ['4','3',ch_43]
outFile.writerow(row)
row = ['4','4',ch_44]
outFile.writerow(row)
row = ['4','5',ch_45]
outFile.writerow(row)
row = ['4','6',ch_46]
outFile.writerow(row)
row = ['4','7',ch_47]
outFile.writerow(row)
row = ['4','8',ch_48]
outFile.writerow(row)
row = ['4','9',ch_49]
outFile.writerow(row)
row = ['4','10',ch_410]
outFile.writerow(row)

row = ['5','1',ch_51]
outFile.writerow(row)
row = ['5','2',ch_52]
outFile.writerow(row)
row = ['5','3',ch_53]
outFile.writerow(row)
row = ['5','4',ch_54]
outFile.writerow(row)
row = ['5','5',ch_55]
outFile.writerow(row)
row = ['5','6',ch_56]
outFile.writerow(row)
row = ['5','7',ch_57]
outFile.writerow(row)
row = ['5','8',ch_58]
outFile.writerow(row)
row = ['5','9',ch_59]
outFile.writerow(row)
row = ['5','10',ch_510]
outFile.writerow(row)

row = ['6','1',ch_61]
outFile.writerow(row)
row = ['6','2',ch_62]
outFile.writerow(row)
row = ['6','3',ch_63]
outFile.writerow(row)
row = ['6','4',ch_64]
outFile.writerow(row)
row = ['6','5',ch_65]
outFile.writerow(row)
row = ['6','6',ch_66]
outFile.writerow(row)
row = ['6','7',ch_67]
outFile.writerow(row)
row = ['6','8',ch_68]
outFile.writerow(row)
row = ['6','9',ch_69]
outFile.writerow(row)
row = ['6','10',ch_610]
outFile.writerow(row)

row = ['7','1',ch_71]
outFile.writerow(row)
row = ['7','2',ch_72]
outFile.writerow(row)
row = ['7','3',ch_73]
outFile.writerow(row)
row = ['7','4',ch_74]
outFile.writerow(row)
row = ['7','5',ch_75]
outFile.writerow(row)
row = ['7','6',ch_76]
outFile.writerow(row)
row = ['7','7',ch_77]
outFile.writerow(row)
row = ['7','8',ch_78]
outFile.writerow(row)
row = ['7','9',ch_79]
outFile.writerow(row)
row = ['7','10',ch_710]
outFile.writerow(row)

row = ['8','1',ch_81]
outFile.writerow(row)
row = ['8','2',ch_82]
outFile.writerow(row)
row = ['8','3',ch_83]
outFile.writerow(row)
row = ['8','4',ch_84]
outFile.writerow(row)
row = ['8','5',ch_85]
outFile.writerow(row)
row = ['8','6',ch_86]
outFile.writerow(row)
row = ['8','7',ch_87]
outFile.writerow(row)
row = ['8','8',ch_88]
outFile.writerow(row)
row = ['8','9',ch_89]
outFile.writerow(row)
row = ['8','10',ch_810]
outFile.writerow(row)

row = ['9','1',ch_91]
outFile.writerow(row)
row = ['9','2',ch_92]
outFile.writerow(row)
row = ['9','3',ch_93]
outFile.writerow(row)
row = ['9','4',ch_94]
outFile.writerow(row)
row = ['9','5',ch_95]
outFile.writerow(row)
row = ['9','6',ch_96]
outFile.writerow(row)
row = ['9','7',ch_97]
outFile.writerow(row)
row = ['9','8',ch_98]
outFile.writerow(row)
row = ['9','9',ch_99]
outFile.writerow(row)
row = ['9','10',ch_910]
outFile.writerow(row)

row = ['10','1',ch_101]
outFile.writerow(row)
row = ['10','2',ch_102]
outFile.writerow(row)
row = ['10','3',ch_103]
outFile.writerow(row)
row = ['10','4',ch_104]
outFile.writerow(row)
row = ['10','5',ch_105]
outFile.writerow(row)
row = ['10','6',ch_106]
outFile.writerow(row)
row = ['10','7',ch_107]
outFile.writerow(row)
row = ['10','8',ch_108]
outFile.writerow(row)
row = ['10','9',ch_109]
outFile.writerow(row)
row = ['10','10',ch_1010]
outFile.writerow(row)

print("--- %s seconds ---" % (time.time() - start_time))

