### source: http://chrisstrelioff.ws/sandbox/2014/11/13/getting_started_with_latent_dirichlet_allocation_in_python.html

### running lda on the documents and checking the topic overlap
import lda
import textmining
import numpy as np
import csv
import matplotlib.pyplot as plt

tdm = textmining.TermDocumentMatrix()

f1 = open(os.path.join('allfiles', 'document01-finance.txt'), "r")
f2 = open(os.path.join('allfiles', 'document02-finance.txt'), "r")
f3 = open(os.path.join('allfiles', 'document03-finance.txt'), "r")
f4 = open(os.path.join('allfiles', 'document04-ee.txt'), "r")
f5 = open(os.path.join('allfiles', 'document05-ee.txt'), "r")

readfile_1 = f1.read()
tdm.add_doc(readfile_1)

readfile_2 = f2.read()
tdm.add_doc(readfile_2)

readfile_3 = f3.read()
tdm.add_doc(readfile_3)

readfile_4 = f4.read()
tdm.add_doc(readfile_4)

readfile_5 = f5.read()
tdm.add_doc(readfile_5)

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

model = lda.LDA(n_topics=2, n_iter=500, random_state=1)
model.fit(data)

topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))

n_top_words = 5

for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    

# use matplotlib style sheet
try:
    plt.style.use('ggplot')
except:
    # version of matplotlib might not be recent
    pass

doc_topic = model.doc_topic_
print("type(doc_topic): {}".format(type(doc_topic)))
print("shape: {}".format(doc_topic.shape))

f, ax= plt.subplots(2, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([1, 2]):
    ax[i].stem(doc_topic[k,:], linefmt='r-',
               markerfmt='ro', basefmt='w-')
    ax[i].set_xlim(-1, 21)
    ax[i].set_ylim(0, 1)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("Document {}".format(k))

ax[1].set_xlabel("Topic")

plt.tight_layout()
plt.show()