import math
import os
import nltk
from nltk.probability import FreqDist

### global vars
pd_x1 = []
pd_x2 = []
pd_x3 = []
pd_x4 = []
pd_x5 = []
s = [] ### corpus codebook


'''
function to calculate probability distribution of various files
'''
def probDist():

    ### files pointers to reading files
    f1 = open(os.path.join('allfiles', 'document01-finance.txt'), "r")
    f2 = open(os.path.join('allfiles', 'document02-finance.txt'), "r")
    f3 = open(os.path.join('allfiles', 'document03-finance.txt'), "r")
    f4 = open(os.path.join('allfiles', 'document04-ee.txt'), "r")
    f5 = open(os.path.join('allfiles', 'document05-ee.txt'), "r")
     
    ### read the file content
    line1 = f1.read()
    line2 = f2.read()
    line3 = f3.read()
    line4 = f4.read()
    line5 = f5.read()
    
    
    ### document01-finance.txt is the writer document and other files are 
    ### are reader files so we get the word list from the write document 
    words = line1.split()
    X_words = []
    
    ### create a dictionary to store the frequency of each term
    dict_x1 = {}
    
    ### using nltk calcuate frequency of each word
    unigramWordList = FreqDist(words)
    datalen = len(unigramWordList) ### total words in the document
    
    for k,v in unigramWordList.items():
        #print k,v
        X_words.append(k)
        dict_x1[k] = (v/float(datalen))
        pd_x1.append(v/float(datalen))
    #print X_words
    #print dict_x1
    #print pd_x1
    
    ### create probability distribution of all files
    for word in X_words:
        pd_x2.append( line2.count(word)/float(datalen) )
        pd_x3.append( line3.count(word)/float(datalen) )
        pd_x4.append( line4.count(word)/float(datalen) )
        pd_x5.append( line5.count(word)/float(datalen) )
        
    #print pd_x2
    #print pd_x3
        
    ### calculate total probability distribution across 3 files
    line_S = line1+line2+line3+line4+line5
    #print line_S
    
    for word in X_words:
        s.append( line_S.count(word)/float(datalen) )
    
    print s

def calcCulturalHole():
    
    p_x = pd_x1  ### codebook for px
    p_y = pd_x5  ### codebook for py
    
    ### calculate shannon entropy
    H_x = 0
    for p in p_x:
         H_x += - p * math.log(p, 2)
    print H_x
    
    ### calculate KL divergence
    
    ### teleporation paramerte with value of 1 percent 
    alpha = 0.01
    
    p_xs = []
    p_ys = []
    iterator = len(p_x)
    i = 0
    while(i < iterator):
        p_xs.append( (p_x[i] * 0.9) + (s[i] * 0.1) )
        p_ys.append( (p_y[i] * 0.9) + (s[i] * 0.1) )
        i = i+1
    
    print p_xs
    print p_ys
    
    ### KL divergence 
    Q_xy = 0
    iterator = len(p_xs)
    i = 0
    while(i < iterator):
        try:
            Q_xy += - p_xs[i] * math.log(p_ys[i], 2)
        except:
            Q_xy += 0
        print Q_xy
        i = i+1
    print Q_xy
    
    
    ### cultural hole
    E_xy = H_x/Q_xy
    print E_xy
    
    C_xy = 1 - E_xy
    
    print ('Cultural hole: %f' % C_xy)

probDist()
calcCulturalHole()
