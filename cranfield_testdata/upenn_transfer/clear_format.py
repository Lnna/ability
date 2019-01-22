from os import path
from nltk.corpus.reader.util import find_corpus_fileids
from nltk.tree import Tree
from nltk.data import FileSystemPathPointer
from stanfordcorenlp.corenlp import StanfordCoreNLP
home_dir=path.join(path.dirname(__file__),'./')

def ctb_clear():
    ctb_dir = path.join(home_dir,'normal_ctb_test')
    reg = '(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*'
    # reg='.*dev'
    ctb_dir = FileSystemPathPointer(ctb_dir)
    fileids = find_corpus_fileids(root=ctb_dir, regexp=reg)
    for fid in fileids:
        f1=open('normal_ctb_test/'+fid,mode='r')
        f2=open('for_clearnlp/'+fid,mode='w')
        for line in f1.readlines():
            if line.find('<S>')>=0 or line.find('</S>')>=0:
                continue
            f2.write(line)
        f1.close()
        f2.close()

def static_dp():
    ctb_dir = path.join(home_dir, 'for_clearnlp')
    # reg = '(.*nw)*(.*bn)*(.*mz)*(.*bc)*(.*wb)*'
    reg = '(.*dep)*'
    ctb_dir = FileSystemPathPointer(ctb_dir)
    fileids = find_corpus_fileids(root=ctb_dir, regexp=reg)
    ct=0
    for fid in fileids:
        f2 = open('for_clearnlp/' + fid, mode='r')
        for line in f2.readlines():
            if line=='\n':
                ct+=1

        f2.close()
    print(ct)

static_dp()