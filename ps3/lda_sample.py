import lda
import textmining
import numpy as np
import csv

'''
    function to output topics across various document given number of topics 
    and term document matrix
'''
def findTopics(tdm,numOfTopics):
    #print type(tdm)
    #print tdm.shape
    
    tdm.write_csv('tdmResult.csv', cutoff=1)
    
    vocab = []
    fp = csv.reader(open('tdmResult.csv','rb'))
    for row in fp:
        vocab = row
        break
    vocab = tuple(vocab)
    
    data = np.genfromtxt('tdmResult.csv', dtype=None, delimiter=',', skip_header=1)
    
    model = lda.LDA(n_topics=numOfTopics, n_iter=500, random_state=1)
    model.fit(data)
    
    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))
    
    for n in range(5):
        sum_pr = sum(topic_word[n,:])
        print("topic: {} sum: {}".format(n, sum_pr))
    n_top_words = 8    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    
    
    
'''
function to create a term document matrix from various documents
'''
def create_tdm():
    
    ### var to build the term document matrix
    tdm = textmining.TermDocumentMatrix()
    
    ### file pointers to open and read all the files
    f1 = open("6334220.txt", 'rb')
    f2 = open("6334221.txt", 'rb')
    f3 = open("6334222.txt", 'rb')
    f4 = open("6334223.txt", 'rb')
    f5 = open("6334224.txt", 'rb')
    f6 = open("6334225.txt", 'rb')
    f7 = open("6334226.txt", 'rb')
    f8 = open("6334227.txt", 'rb')
    f9 = open("6334226.txt", 'rb')
    f10 = open("6334227.txt", 'rb')
    
    ### add the file content to the tdm var
    read_file01 = f1.read()
    tdm.add_doc(read_file01)
    
    read_file02 = f2.read()
    tdm.add_doc(read_file02)
    
    read_file03 = f3.read()
    tdm.add_doc(read_file03)
    
    read_file04 = f4.read()
    tdm.add_doc(read_file04)
    
    read_file05 = f5.read()
    tdm.add_doc(read_file05)
    
    read_file06 = f6.read()
    tdm.add_doc(read_file06)
    
    read_file07 = f7.read()
    tdm.add_doc(read_file07)
    
    read_file08 = f8.read()
    tdm.add_doc(read_file08)
    
    read_file09 = f9.read()
    tdm.add_doc(read_file09)
    
    read_file10 = f10.read()
    tdm.add_doc(read_file10)
    
    return tdm
    
    
def __main__():
    numOfTopics = 20
    findTopics( create_tdm() , numOfTopics )