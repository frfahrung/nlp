import math
import glob
import os
import json
import numpy
import re

docList = glob.glob(os.path.join('./training_data', '*.json'))
# docList = glob.glob(os.path.join('./testing_data', '*.json'))
vocab = [line.rstrip() for line in open('vocabulary.txt')]
idfVector = [line.rstrip() for line in open('idf_train.txt')]
# idfVector = [line.rstrip() for line in open('idf_test.txt')]

def getWordList(doc):
    wordList = []
    with open(doc) as json_data:
        content = json.load(json_data, strict=False)
        for sentence in content["sentences"]:
            for words in sentence["tokens"]:
                word = words["originalText"]
                wordList.append(word)
    return wordList

def TF( word, wordList):
    return wordList.count(word)

def TFvector(doc):
    tfVector = []
    wordList = getWordList(doc)
    for word in vocab:
        tfVector.append(TF(word, wordList))
    return tfVector

def savetocsvfile(IDFInput):
    numpy.savetxt("LTC_train.csv", IDFInput, fmt='%4.4f', delimiter=",")
    # numpy.savetxt("LTC_test.csv", IDFInput, fmt='%4.4f', delimiter=",")

def LTCdocVector():
    numOfDoc = len(docList)
    numOfVocab = len(vocab)
    ltc = numpy.zeros((numOfDoc,numOfVocab+1))

    pattern = re.compile("[\.\/training_data\/]+[5].*")
    # pattern = re.compile("[\.\/test_data\/]+[5].*")

    for i in range(len(docList)):
        print (i)
        wordList = getWordList(docList[i])
        temp2 = 0
        temp3 = []
        tfVector = TFvector(docList[i])
        for k in range(len(vocab)):
            temp1 = math.log10(tfVector[k]+1.0)*float(idfVector[k])
            temp2 += math.pow(temp1,2)
            temp3.append(temp1)
        temp4 = math.sqrt(temp2)
        for j in range(len(vocab)):
            ltc[i][j] = temp3[j]/temp4
        if pattern.match(docList[i]):
            ltc[i][numOfVocab] = 0
        else:
            ltc[i][numOfVocab] = 1
    return ltc

savetocsvfile(LTCdocVector())
