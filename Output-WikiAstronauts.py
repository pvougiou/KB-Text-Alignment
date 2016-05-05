import math
import pandas as pd
pd.set_option('display.max_colwidth', -1)

import re
from nltk.tokenize import RegexpTokenizer
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
import sys
import glob
import shutil
import cPickle as pickle

# Useful for .xml files manipulation
import dicttoxml
from xml.dom import minidom
import xml.etree.ElementTree as ET

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


csv_dir = 'CrowdFlower/WikiAstronauts/f900315.csv'
output_csv_dir = 'Output/WikiAstronauts/Output.xls'
output_xml_dir = 'Output/WikiAstronauts/Output.xml'
output_eval_dir = 'Output/WikiAstronauts/Evaluation.xls'
cache_dir = 'Caches/WikiAstronauts/'

num_tokens = []


def load_cache():
    if os.path.isfile(cache_dir + 'dataset-WikiAstronauts.p') :
        temp = pickle.load(open(cache_dir + 'dataset-WikiAstronauts.p', "rb"))
    else:
        temp = []
    return temp


def shortest_length(sentences):
    vectorizer = CountVectorizer(min_df=1, token_pattern='\w+', lowercase=True)
    train = vectorizer.fit_transform(sentences)
    num_samples, num_features = train.shape
    length = np.zeros(num_samples)
    for i in range(0, num_samples):
        length[i] = sp.linalg.norm(train.getrow(i).toarray())
    return sentences[np.argmin(length)]
  

# Computes distance on the normalised vectors
def distance(v1, v2):
    v1_normalized = v1/sp.linalg.norm(v1)
    v2_normalized = v2/sp.linalg.norm(v2)
    delta = v1_normalized - v2_normalized
    return sp.linalg.norm(delta)


def get_original(sentence):
    while sentence.find('<') > -1:
        start_flag = sentence.find('<')
        end_flag = sentence.find('>')
        sentence = sentence.replace(sentence[start_flag:end_flag + 1], '')
    return sentence


def shortening(sentences):
    vectorizer = CountVectorizer(min_df=1, token_pattern='\w+', lowercase=True)
    train = vectorizer.fit_transform(sentences)
    num_samples, num_features = train.shape
    count = np.zeros(num_samples)
    for i in range(0, num_samples):

            count[i] = count[i] + np.sum(train.getrow(i).toarray())

    avg = np.sum(count) / float(num_samples)
    extent = np.zeros(num_samples)
    for i in range(0, num_samples):
        extent[i] = 1 / (1 * np.sqrt(2 * np.pi)) * np.exp( - (count[i] - avg)**2 / (2 * 1**2) )
    #plt.plot(count, extent, 'o')
    #plt.show()
    return [extent[sentence] for sentence in range(0, extent.shape[0])]


def baseline(sentences):
    count = np.zeros(len(sentences))
    vectorizer = CountVectorizer(min_df=1, token_pattern='\w+', lowercase=True)
    train = vectorizer.fit_transform(sentences)
    num_samples, num_features = train.shape
    print("#samples: %d, #features: %d" % (num_samples, num_features))
    for i in range(0, num_samples):
        for j in range(0, num_samples):
            if np.array_equal(train.getrow(i).toarray(), train.getrow(j).toarray()):
                count[i] = count[i] + 1
    index = np.argmax(count)
    #print count
    return sentences[index]


def count_tokens(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    return len(tokenizer.tokenize(sentence))


def counter(tensor):
    unique = np.zeros((tensor.shape[0], tensor.shape[1] + 2))
    print unique.shape
    print tensor.shape
    # Flag for the number of duplicates.
    flag = []
    [flag.append(False) for row in range(0, tensor.shape[0])]
    #print flag
     
    for i in range(0, tensor.shape[0]):
        count = 1
        unique[i, :tensor.shape[1]] = tensor.getrow(i).toarray()
        unique[i][tensor.shape[1]] = i
        for j in range(i + 1, tensor.shape[0]):
            if np.array_equal(tensor.getrow(i).toarray(), tensor.getrow(j).toarray()):
                count = count + 1
                flag[j] = True
        unique[i][tensor.shape[1] + 1] = count

    for i in range(len(flag) - 1 , - 1, - 1):
        if flag[i]:
            unique = np.delete(unique, i, 0)
    #print unique
    
    print unique.shape
    #print flag
    return unique


def distance_from_original(initial, simplifications):
    vectorizer = CountVectorizer(min_df=1, token_pattern='\w+', lowercase=True)
    full = simplifications[:]
    #print len(full)
    full.insert(0, initial)
    #print len(full)
    train = vectorizer.fit_transform(full)
    distances = np.zeros(train.shape[0] - 1)
    for i in range(0, train.shape[0] - 1):
        distances[i] = distance(train.getrow(0).toarray(), train.getrow(i + 1).toarray())
    print('Length of distances in function: %d' % (len(distances)))
    return distances


def cluster(sentences):
    vectorizer = CountVectorizer(min_df=1, token_pattern='\w+', lowercase=True)
    train = vectorizer.fit_transform(sentences)
    num_samples, num_features = train.shape
    num_clusters = 4
    uniques = counter(train)
    if math.ceil(uniques.shape[0] / 3.0) < 2:
        num_clusters = uniques.shape[0]
    else:
        num_clusters = int(math.ceil (uniques.shape[0] / 3.0))
    km = KMeans(n_clusters=num_clusters, init='random', n_init=1, verbose=1)
    km.fit(uniques[:, :uniques.shape[1] - 2])

    total = np.zeros(km.labels_.shape[0])
    for i in range(0, km.labels_.shape[0]):
        for j in range(0, km.labels_.shape[0]):
            if km.labels_[j] == km.labels_[i]:
                total[i] = total[i] + uniques[i][uniques.shape[1] - 1]
    indeces = []
    for i in range(0, km.labels_.shape[0]):
        if km.labels_[np.argmax(total)] == km.labels_[i]:
            indeces.append(int(uniques[i][uniques.shape[1] - 2]))
    #print indeces
    
    return [sentences[j] for j in indeces]


def get_annotations(sentence):
    annotations = []
    print sentence
    while sentence.find('<b><font color="purple">') > -1:
        start_flag = sentence.find('<b><font color="purple">') + len('<b><font color="purple">')
        end_flag = sentence.find('</font></b>')
        
        annotations.append(sentence[start_flag:end_flag])
        sentence = sentence[:start_flag - len('<b><font color="purple">')] + sentence[start_flag:end_flag] + sentence[end_flag + len('</font></b>'):]
        #print sentence
    return annotations


csv = pd.read_csv(csv_dir, header=0, usecols = ['result1', 'sentence'], skip_blank_lines=False)

dictionary = load_cache()
if len(dictionary) == 0:
    raw_input('Cache file: ' + cache_dir +  "dataset-WikiAstronauts.p was not found. You should try to execute Dataset-WikiAstronauts.py first. Press Enter to kill this process...")
    sys.exit()
else:
    raw_input('Cache file: ' + cache_dir +  'dataset-WikiAstronauts.p has been loaded successfully. Press Enter to continue...')


"""

for i in range(0, len(csv.sentence)):
    csv.sentence[i] = get_original(csv.sentence[i])
print csv

"""

flag = 0
sentences = {}

for i in range(0, len(csv.sentence)):
    if csv.sentence[i] not in sentences:
        sentences[csv.sentence[i]] = [csv.result1[i]]
    else:
        sentences[csv.sentence[i]].append(csv.result1[i])
        

# Get results according to the baseline approach.
baseline_result = {}
for original in sentences:
    baseline_result[original] = baseline(sentences[original])


# Get results according to the k-means clustering approach.
result = {}
for original in sentences:
    result[original] = cluster(sentences[original])

    
ratios = {}
for original in sentences:
    num_highlighted = []
    annotations = get_annotations(original)
    for i in range(0 , len(result[original])):
        tmp = result[original][i].lower().replace(',', '')
        num_highlighted.append(0)
        #print annotations
        for j in range(0, len(annotations)):
            position = tmp.find(annotations[j].lower())
            if position > -1:
                if position == 0 and  tmp.find(annotations[j].lower() + ' ') > -1:
                    start_flag = tmp.find(annotations[j].lower() + ' ')

                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1
                elif (position == len(tmp) - len(annotations[j]) or position == len(tmp) - len(annotations[j]) - 1) and tmp.find(' ' + annotations[j].lower()) > -1:
                    start_flag = tmp.find(' ' + annotations[j].lower())

                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1
                elif tmp.find(' ' + annotations[j].lower() + ' ') > -1:
                    start_flag = tmp.find(' ' + annotations[j].lower() + ' ')
                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1


        num_highlighted[i] = num_highlighted[i] / float(len(annotations))
                
                
    ratios[original] = num_highlighted


integrity = {}
distances = {}
shortening_extent = {}
for original in sentences:

    distances[original] = distance_from_original(get_original(original), result[original])
    shortening_extent[original] = shortening(result[original])
    num_additional = []
    initial = get_original(original).lower().replace(',', '').replace('.', '').split()

    for i in range(0 , len(result[original])):
        tmpInitial = initial
        tmp = result[original][i].lower().replace(',', '').replace('.', '').split()
        num_additional.append(0)
        for j in range(0, len(tmp)):
            if tmp[j] not in tmpInitial:
                num_additional[i] = num_additional[i] + 1
            else:
                tmpInitial.remove(tmp[j])
                

        num_additional[i] = 1.0 - (num_additional[i] / float(len(tmp)))
                
    #print('Length of distances: %d' % (len(distances[original])))
    #print('Length of shortening: %d' % (len(shortening_extent[original])))
    #print('Length of num_additional: %d' % (len(num_additional)))
    #print('Length of shortening: %d' % (len(shortening_extent[original])))
    #print('Length of result[original]: %d' % (len(result[original])))

           
    integrity[original] = num_additional
    #print('Length of integrity: %d' % (len(integrity[original])))
 

score = {}
for original in sentences:
    score[original] = []
    for j in range(0, len(result[original])): 
        score[original].append(shortening_extent[original][j] * (math.exp(ratios[original][j] * integrity[original][j] * distances[original][j])))


unclustered_ratios = {}
for original in sentences:
    num_highlighted = []
    annotations = get_annotations(original)
    for i in range(0 , len(sentences[original])):
        tmp = sentences[original][i].lower().replace(',', '')
        num_highlighted.append(0)
        print annotations
        for j in range(0, len(annotations)):
            position = tmp.find(annotations[j].lower())
            if position > -1:
                if position == 0 and  tmp.find(annotations[j].lower() + ' ') > -1:
                    start_flag = tmp.find(annotations[j].lower() + ' ')

                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1
                elif (position == len(tmp) - len(annotations[j]) or position == len(tmp) - len(annotations[j]) - 1) and tmp.find(' ' + annotations[j].lower()) > -1:
                    start_flag = tmp.find(' ' + annotations[j].lower())

                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1
                elif tmp.find(' ' + annotations[j].lower() + ' ') > -1:
                    start_flag = tmp.find(' ' + annotations[j].lower() + ' ')
                    tmp = tmp[:start_flag] + tmp[start_flag + len(annotations[j]) + 1:]

                    num_highlighted[i] = num_highlighted[i] + 1


        num_highlighted[i] = num_highlighted[i] / float(len(annotations))
                
                
    unclustered_ratios[original] = num_highlighted


unclustered_integrity = {}
unclustered_distances = {}
unclustered_shortening_extent = {}
for original in sentences:

    unclustered_distances[original] = distance_from_original(get_original(original), sentences[original])
    unclustered_shortening_extent[original] = shortening(sentences[original])
    num_additional = []
    initial = get_original(original).lower().replace(',', '').replace('.', '').split()

    for i in range(0 , len(sentences[original])):
        tmpInitial = initial
        tmp = sentences[original][i].lower().replace(',', '').replace('.', '').split()
        num_additional.append(0)
        for j in range(0, len(tmp)):
            if tmp[j] not in tmpInitial:
                num_additional[i] = num_additional[i] + 1
            else:
                tmpInitial.remove(tmp[j])
                

        num_additional[i] = 1.0 - (num_additional[i] / float(len(tmp)))
                
    print('Length of distances: %d' % (len(unclustered_distances[original])))
    print('Length of num_additional: %d' % (len(num_additional)))
    print('Length of shortening: %d' % (len(unclustered_shortening_extent[original])))
    print('Length of result[original]: %d' % (len(sentences[original])))
 
    unclustered_integrity[original] = num_additional
    print('Length of integrity: %d' % (len(unclustered_integrity[original])))
 

unclustered_score = {}
clustered_distances = {}
unclustered_conformity = {}
for original in sentences:
    clustered_distances[original] = shortest_length(result[original])
    unclustered_conformity[original] = []
    unclustered_score[original] = []
    for j in range(0, len(sentences[original])):
        unclustered_conformity[original].append(math.exp(unclustered_ratios[original][j] * unclustered_integrity[original][j]))
        unclustered_score[original].append(unclustered_shortening_extent[original][j] * (math.exp(unclustered_ratios[original][j] * unclustered_integrity[original][j] * unclustered_distances[original][j])))
    
    


"""

#

evaluation={'Annotated Sentence': [], '#1 Simplification': [], '#1 Rating': [], '#2 Simplification': [], '#2 Rating': [], '#3 Simplification': [], '#3 Rating': [], '#4 Simplification': [], '#4 Rating': [],\
        '#5 Simplification': [], '#5 Rating': [], '#6 Simplification': [], '#6 Rating': [], '#7 Simplification': [], '#7 Rating': []}
indeces_eval_sentences = []
num_eval_sentences = 0
while num_eval_sentences < 30:
    random = np.random.randint(0, len(output['Annotated Sentence']))
    if random not in indeces_eval_sentences:
        
        key = output['Annotated Sentence'][random]
        evaluation['Annotated Sentence'].append(key.replace('\t', ''))
        evaluation['#1 Simplification'].append(unicode(result[key][score[key].index(max(score[key]))], 'ascii', errors='ignore'))
        evaluation['#1 Rating'].append(0)
        evaluation['#2 Simplification'].append(unicode(sentences[key][unclustered_score[key].index(max(unclustered_score[key]))], 'ascii', errors='ignore'))
        evaluation['#2 Rating'].append(0)
        evaluation['#3 Simplification'].append(unicode(sentences[key][unclustered_integrity[key].index(max(unclustered_integrity[key]))], 'ascii', errors='ignore'))
        evaluation['#3 Rating'].append(0)
        evaluation['#4 Simplification'].append(unicode(sentences[key][unclustered_shortening_extent[key].index(max(unclustered_shortening_extent[key]))], 'ascii', errors='ignore'))
        evaluation['#4 Rating'].append(0)
        evaluation['#5 Simplification'].append(unicode(sentences[key][unclustered_conformity[key].index(max(unclustered_conformity[key]))], 'ascii', errors='ignore'))
        evaluation['#5 Rating'].append(0)
        evaluation['#6 Simplification'].append(unicode(baseline_result[key], 'ascii', errors='ignore'))
        evaluation['#6 Rating'].append(0)
        evaluation['#7 Simplification'].append(unicode(clustered_distances[key], 'ascii', errors='ignore'))
        evaluation['#7 Rating'].append(0)
        num_eval_sentences = num_eval_sentences + 1
        indeces_eval_sentences.append(random)

    
eval_df = pd.DataFrame(evaluation, index=[i for i in range(0, len(evaluation['Annotated Sentence']))], columns=['Annotated Sentence', '#1 Simplification', '#1 Rating', '#2 Simplification', '#2 Rating', '#3 Simplification', '#3 Rating', '#4 Simplification', '#4 Rating', '#5 Simplification', '#5 Rating', '#6 Simplification', '#6 Rating', '#7 Simplification', '#7 Rating'])
eval_df.to_html(output_eval_dir, index=False, escape=False)

"""

output={'Annotated Sentence': [], 'Simplification': []}
for original in sentences:
    output['Annotated Sentence'].append(original)
    output['Simplification'].append(unicode(result[original][score[original].index(max(score[original]))], 'ascii', errors='ignore'))
    num_tokens.append(count_tokens(result[original][score[original].index(max(score[original]))]))
    
print('Total number of tokens of the simplifications: %d' % (sum(num_tokens)))

output_df = pd.DataFrame(output, index=[i for i in range(0, len(output['Annotated Sentence']))])
output_df['Annotated Sentence'] = output_df['Annotated Sentence'].replace(to_replace='\t', value='', regex=True)
output_df.to_html(output_csv_dir, index=False, escape=False)



tokenizer = RegexpTokenizer(r'\w+')
for i in range(0, len(dictionary)):
    flag = False
    for original in output['Annotated Sentence']:
        if tokenizer.tokenize(dictionary[i]['value']) == tokenizer.tokenize(get_original(original)):
            dictionary[i]['simplification'] = result[original][score[original].index(max(score[original]))]
            flag = True
            break
    if flag is False:
        print dictionary[i]['annotated_sentence']


xml_dict = []
for i in range(0 , len(dictionary)):
    xml_dict.append({'annotated_sentence': dictionary[i]['annotated_sentence'], \
                     'value': dictionary[i]['value'], \
                     'triples': dictionary[i]['triples'], \
                     'simplification': dictionary[i]['simplification']})
        
xml = dicttoxml.dicttoxml(xml_dict, attr_type=False, custom_root='WikiAstronauts')
root = ET.fromstring(xml)
for i in range(0, len(root)):
    root[i][2], root[i][3] = root[i][3], root[i][2]
    root[i][2], root[i][1] = root[i][1], root[i][2]
    root[i][0], root[i][1] = root[i][1], root[i][0]
for child in root:
    child.tag = 'sentence'
    for grandchild in child:
        if grandchild.tag == 'triples':
            for item in grandchild:
                item.tag = 'triple'
tree = ET.ElementTree(root)
tree.write(output_xml_dir, encoding='utf-8', xml_declaration=True)
xml = minidom.parse(output_xml_dir)
dom = xml.toprettyxml(encoding='utf-8')    

with open(output_xml_dir, "w") as xml_file:
    xml_file.write(dom)
    xml_file.close()
    
