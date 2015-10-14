#!/usr/bin/env python

import json
from modules.exportgraph import mtgx2json
import glob
import os.path
import time

folder = 'output/'


def list_graphs():
    filelist = []
    files = glob.glob('output/*.json')
    for i in files:
        record = i.split('/')[-1], time.ctime(os.path.getctime(i))
        filelist.append(record)
    return filelist


def graph_json(graph, filename):
    filename = str(filename).split('/')[-1].replace('.mtgx', '.json', 1)
    path = '%s%s' % (folder, filename)
    g = mtgx2json(graph)
    f = open(path, 'a')
    f.write(json.dumps(g, indent=4))
    f.close()
