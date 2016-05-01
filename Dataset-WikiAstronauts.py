#from lxml import etree
#from codecs import open
import xml.etree.ElementTree as ET
import csv
import re
from nltk.tokenize import RegexpTokenizer
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import os
import glob
import shutil

xml_dir = 'Data/WikiAstronauts/XML/'
csv_dir = 'Data/wikiAstronauts/CSV/'
exp_dir = 'CrowdFlower/WikiAstronauts/'


num_files = 0
processed_files = 0

num_sentences = 0
included_sentences = [0, 0, 0]
facts = 0
processed_facts = 0
tokens_triples = []
num_triples = []
num_tokens = []
unique_predicates = []
predicates = {}
num_annotations = 0


def annotate(text):
    while text.find('[[') > -1:
        start_flag = text.find('[[')
        or_flag = text.find('|')
        end_flag = text.find(']]')
        text = text.replace('[[', '<b><font color="purple">', 1)
        text = text.replace(text[or_flag + len('<b><font color="purple">') - 2 :end_flag + len('<b><font color="purple">') - 2 + 2], '</font></b>', 1)
    return text


def get_annotations(filename, sentence):
    total = 0
    add_annotations(filename, sentence)
    while sentence.find('[[') > -1:
        sentence = sentence.replace('[[', '', 1)
        total = total + 1
    return total


def get_predicate(triple):
    start_flag = triple.find(' ')
    tmp = triple.replace(' ', '', 1)
    end_flag = tmp.find(' ')
    return triple[start_flag + 1:end_flag + 1]
    

def construct_graph_token_triples(data):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    x = np.arange(min(data), max(data) + 5, 5)
    total = {item: 0 for item in x}
    
    for item in data:
        for i in range(0, len(x)):
            if item <= x[i]:
                total[x[i]] = total[x[i]] + 1
                break
    y = []
    for item in x:
        y.append(total[item])
    print(x)
    print(y)
    plt.plot(x, y, '-o', color='b', linewidth=2.0)
    plt.xlabel(r'$^{\textrm{Number of Tokens}}/_{\textrm{Number of Triples}}$')
    plt.ylabel("Number of Sentences")
    plt.grid()
    plt.show()

    
def construct_graph_triples(data):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    x = np.arange(min(data), max(data) + 1, 1)
    total = {item: 0 for item in x}
    
    for item in data:
        for i in range(0, len(x)):
            if item <= x[i]:
                total[x[i]] = total[x[i]] + 1
                break
    y = []
    for item in x:
        y.append(total[item])
    print(x)
    print(y)
    plt.plot(x, y, '-o', color='r', linewidth=2.0)
    
    plt.xlabel("Number of Triples")
    plt.ylabel("Number of Sentences")
    plt.grid()
    plt.show()

    
def construct_graph_tokens(data):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    x = np.arange(min(data), max(data) + 1, 1)
    total = {item: 0 for item in x}
    
    for item in data:
        for i in range(0, len(x)):
            if item <= x[i]:
                total[x[i]] = total[x[i]] + 1
                break
    y = []
    for item in x:
        y.append(total[item])
    print(x)
    print(y)
    plt.plot(x, y, '-o', color='c', linewidth=2.0)
    
    plt.xlabel("Number of Tokens")
    plt.ylabel("Number of Sentences")
    plt.grid()
    plt.show()


def construct_graph_tokens_to_triples(tokens, triples):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')


    plt.plot(tokens, triples, 'o', color='r', linewidth=2.0)
    
    plt.xlabel("Number of Tokens")
    plt.ylabel("Number of Triples")
    plt.grid()
    plt.show()

    
def add_annotations(text, sentence):
    search = ['He', 'She']
    tokenizer = RegexpTokenizer(r'\w+')
    text = text.replace('_', ' ')
    text_tokens = tokenizer.tokenize(text)
    search.extend(text_tokens)
    flag = False
    for entity in search:
        pos = 0
        while sentence[pos:].find(entity) > -1:
            pos = sentence[pos:].find(entity) + pos
            if sentence[pos - 1] != '[' and sentence[pos + len(entity)] == ' ' and (sentence[pos - 1] == ' ' or sentence[pos - 1] == '\t')  and pos >= 1 or \
               sentence[pos + len(entity)] != '|' and sentence[pos + len(entity)] == ' ' and pos == 0:
                
                sentence = sentence[:pos] + '[[' + entity + '|' + entity + ']]' + sentence[pos+len(entity):]
                pos = pos + len('[[' + entity + '|' + entity + ']]')
                flag = True
            else:
                pos = pos + len(entity)

    return sentence
    

def dataset():
    global tokens_triples
    global num_sentences
    global included_sentences
    global processed_facts
    global num_triples
    global num_tokens
    global num_annotations
    global unique_predicates
    global predicates
    
    
    if os.path.exists(exp_dir + 'experiment.csv'):
        os.remove(exp_dir + 'experiment.csv')
    tokenizer = RegexpTokenizer(r'\w+')
    with open(exp_dir + 'experiment.csv', 'wb') as exp_file:
        fieldnames = ['Sentence']
        writer = csv.DictWriter(exp_file, fieldnames = fieldnames)
        writer.writeheader()

        for filename in glob.glob(os.path.join(csv_dir, '*.csv')):
            #print filename
            with open(filename, 'rb') as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_reader.next()
                rows_flag = 0;
                with open(filename.replace('CSV', 'XML').replace('csv', 'xml'), 'r') as xml_file:
                    sentence_number = -1
                    xml = xml_file.read()
                    xml = unicode(xml, 'ascii', errors='ignore')
                    root = ET.fromstring(xml)
                    
                    for row in csv_reader:
                        sentence_number = sentence_number + 1
                        num_sentences = num_sentences + 1
                        """
                        if len(root[sentence_number][5]) >= 1 and row[0].find('?') == -1:
                            rows_flag = rows_flag + 1
                            included_sentences[0] = included_sentences[0] + 1
                            writer.writerow({'Sentence': row[0]})
                            num_triples.append(len(root[sentence_number][5]))
                            num_tokens.append(len(tokenizer.tokenize(root[sentence_number][0].text)))    
                            tokens_triples.append(len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]))
                            processed_facts = processed_facts + len(root[sentence_number][5])
                        """   
                        
                        if len(root[sentence_number][5]) >= 1:
                            if row[0].find('?') == -1 and (len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]) >= 20)  and included_sentences[2] < 200:
                                rows_flag = rows_flag + 1
                                included_sentences[2] = included_sentences[2] + 1
                                writer.writerow({'Sentence': row[0]})
                                #print row[0]
                                num_annotations = num_annotations + get_annotations(filename.rsplit('/',1)[-1], root[sentence_number][2].text)
                                for triple in range(0, len(root[sentence_number][5])):
                                    predicate = get_predicate(root[sentence_number][5][triple].text)
                                    if predicate not in unique_predicates:
                                        unique_predicates.append(predicate)
                                        predicates[predicate] = 1 
                                    else:
                                        predicates[predicate] = predicates[predicate] + 1
                                num_triples.append(len(root[sentence_number][5]))
                                num_tokens.append(len(tokenizer.tokenize(root[sentence_number][0].text)))

                                
                                tokens_triples.append(len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]))
                                #print sentence_number
                                #print xml_file
                                processed_facts = processed_facts + len(root[sentence_number][5])
                            if row[0].find('?') == -1 and (len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]) < 20) \
                               and len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]) >= 10 and included_sentences[1] < 200:
                                rows_flag = rows_flag + 1
                                included_sentences[1] = included_sentences[1] + 1
                                writer.writerow({'Sentence': row[0]})
                                #print row[0]
                                num_annotations = num_annotations + get_annotations(filename.rsplit('/',1)[-1], root[sentence_number][2].text)
                                for triple in range(0, len(root[sentence_number][5])):
                                    predicate = get_predicate(root[sentence_number][5][triple].text)
                                    if predicate not in unique_predicates:
                                        unique_predicates.append(predicate)
                                        predicates[predicate] = 1 
                                    else:
                                        predicates[predicate] = predicates[predicate] + 1

                                num_triples.append(len(root[sentence_number][5]))
                                num_tokens.append(len(tokenizer.tokenize(root[sentence_number][0].text)))

                 
                                tokens_triples.append(len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]))
                                #print sentence_number
                                #print xml_file
                                processed_facts = processed_facts + len(root[sentence_number][5])
                            if row[0].find('?') == -1 and (len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]) < 10) \
                               and len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]) >= 5 and included_sentences[0] < 200:
                                rows_flag = rows_flag + 1
                                included_sentences[0] = included_sentences[0] + 1
                                writer.writerow({'Sentence': row[0]})
                                #print row[0]
                                num_annotations = num_annotations + get_annotations(filename.rsplit('/',1)[-1], root[sentence_number][2].text)
                                for triple in range(0, len(root[sentence_number][5])):
                                    predicate = get_predicate(root[sentence_number][5][triple].text)
                                    if predicate not in unique_predicates:
                                        unique_predicates.append(predicate)
                                        predicates[predicate] = 1 
                                    else:
                                        predicates[predicate] = predicates[predicate] + 1

                                num_triples.append(len(root[sentence_number][5]))
                                num_tokens.append(len(tokenizer.tokenize(root[sentence_number][0].text)))

                                
                                tokens_triples.append(len(tokenizer.tokenize(root[sentence_number][0].text)) / len(root[sentence_number][5]))
                                #print sentence_number
                                #print xml_file
                                processed_facts = processed_facts + len(root[sentence_number][5])
                        
                
                    xml_file.close()
                csv_file.close()
        exp_file.close()
    # It sorts the dictionary of predicates according to the times of occurrence.
    #print sorted(predicates.items(), key=lambda x:x[1])
    print('%d out of the total %d sentences have been included.' % (sum(included_sentences), num_sentences))
    print('Total number of facts-triples that have been included: %d' % (processed_facts))
    print('Total number of tokens of the sentences that have been included: %d' % (sum(num_tokens)))
    print('Total number of arguments of the sentences that have been included: %d' % (num_annotations))
    print('Total number of unique predicates of the sentences that have been included: %d' % (len(unique_predicates)))

    
def main():

    if os.path.exists(csv_dir):
        shutil.rmtree(csv_dir)
    os.makedirs(csv_dir)
    #parser = etree.XMLParser(encoding="utf-8")

    for filename in glob.glob(os.path.join(xml_dir, '*.xml')):
        global num_files
        num_files = num_files + 1
        with open(filename, 'r') as xml_file:
            with open(csv_dir + filename.replace(xml_dir, '').replace('.xml', '.csv'), 'wb') as csv_file:
                fieldnames = ['Sentence']
                writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
                writer.writeheader()

                xml = xml_file.read()
                xml = unicode(xml, 'ascii', errors='ignore')
                try:
                    root = ET.fromstring(xml)
                    global processed_files
                    global facts
                    processed_files = processed_files + 1
                    for i in range(0, len(root)):
                        writer.writerow({'Sentence': annotate(add_annotations(filename.rsplit('/',1)[-1], root[i][2].text))})
                        facts = facts + len(root[i][5])

                    csv_file.close()
                except ET.ParseError:
                    csv_file.close()
                    os.remove(csv_dir + filename.replace(xml_dir, '').replace('.xml', '.csv'))
                    #print(filename + ' has not been included.')
            xml_file.close()
    print('%d / %d XML files have been processed.' % (processed_files, num_files))
    print('Total number of facts-triples that have been processed: %d' % (facts))


main()
dataset()
#construct_graph_token_triples(tokens_triples)
#construct_graph_triples(num_triples)
#construct_graph_tokens(num_tokens)
#construct_graph_tokens_to_triples(num_tokens, num_triples)
