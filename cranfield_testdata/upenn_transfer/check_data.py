# from phrase_trans_copy import parse_trees
import os
from nltk.corpus import BracketParseCorpusReader

dir='/home/lnn/Downloads/ctb_bracket'


def parse_trees(dir,fileid):
    # reader = BracketParseCorpusReader('/home/lnn/Documents/ability/cranfield_testdata/upenn_transfer/new_ctb', fileid)
    reader = BracketParseCorpusReader(dir, fileid)
    tree = reader.parsed_sents()
    return tree

data={}
sum=0
for fid in os.listdir(dir):
    trees=parse_trees(dir,fid)
    for tree in trees:
        tree=tree.__str__()
        if tree in data:
            # print(fid,data[tree],tree)
            sum+=1
            continue
        else:
            data[tree]=fid

print(sum)
print(len(data))