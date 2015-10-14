#!/usr/bin/env python

from modules.exportgraph import mtgx2json
import sys
import json

folder = 'output/'

if len(sys.argv) != 2:
    print 'Usage: ./pandora testgraph.mtgz'
    sys.exit(1)

g = sys.argv[1]


def graph_json(graph):
    print '[+] Starting Graph export....'
    filename = str(graph).split('/')[-1].replace('.mtgx', '.json', 1)
    path = '%s%s' % (folder, filename)
    print '[-] Saving graph to %s' % path
    g = mtgx2json(graph)
    f = open(path, 'a')
    f.write(json.dumps(g, indent=4))
    f.close()
    print '[!] Graph export complete'

if __name__ == '__main__':
    graph_json(g)
