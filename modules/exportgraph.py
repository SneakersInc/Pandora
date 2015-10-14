#!/usr/bin/env python

# Original code was created by Nadeem Douba as part of the Canari Framework


from collections import OrderedDict
from xml.etree.cElementTree import XML
from zipfile import ZipFile


def mtgx2json(graph):
    zipfile = ZipFile(graph)
    graphs = filter(lambda x: x.endswith('.graphml'), zipfile.namelist())
    for f in graphs:
        multikeys = []
        xml = XML(zipfile.open(f).read())
        links = {}
        for edge in xml.findall('{http://graphml.graphdrawing.org/xmlns}graph/'
                                '{http://graphml.graphdrawing.org/xmlns}edge'):
            src = edge.get('source')
            dst = edge.get('target')
            if src not in links:
                links[src] = dict(in_=[], out=[])
            if dst not in links:
                links[dst] = dict(in_=[], out=[])
            links[src]['out'].append(dst)
            links[dst]['in_'].append(src)

        for node in xml.findall('{http://graphml.graphdrawing.org/xmlns}graph/'
                                '{http://graphml.graphdrawing.org/xmlns}node'):

            node_id = node.get('id')
            node = node.find('{http://graphml.graphdrawing.org/xmlns}data/'
                             '{http://maltego.paterva.com/xml/mtgx}MaltegoEntity')

            record = OrderedDict({'NodeID': node_id, 'EntityType': node.get('type').strip()})
            props = {'Data': {}}
            for prop in node.findall('{http://maltego.paterva.com/xml/mtgx}Properties/'
                                     '{http://maltego.paterva.com/xml/mtgx}Property'):
                value = prop.find('{http://maltego.paterva.com/xml/mtgx}Value').text or ''
                entity_prop = {prop.get('displayName'): value.strip()}
                props['Data'].update(entity_prop)
            record.update(props)
            s = ' - '.join(['%s: %s' % (key, value) for (key, value) in record['Data'].items()])
            record.pop('Data')
            data = {'Data': s}
            record.update(data)
            link = {'Links': {}}
            i_link = {'Incoming': links.get(node_id, {}).get('in_', 0)}
            link['Links'].update(i_link)
            o_link = {'Outgoing': links.get(node_id, {}).get('out', 0)}
            link['Links'].update(o_link)
            record.update(link)
            multikeys.append(record)
        return multikeys
