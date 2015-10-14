#!/usr/bin/env python


from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from core import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    l = list_graphs()
    return render_template('home.html', list=l)


@app.route('/graph/<filename>', methods=['GET'])
def graph(filename):
    g = 'output/%s' % filename
    in_file = open(g, 'r')
    new_dict = json.load(in_file)
    in_file.close()
    return render_template('graph.html', filename=filename, output=new_dict)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        f = request.files['file']
        filename = secure_filename(f.filename)
        graph_json(f, filename)
        return redirect('/', code=302)
    except Exception as e:
        return render_template('404.html', error=e)


@app.route('/graph/<filename>/<direction>/<nodeid>', methods=['GET'])
def get_links(filename, direction, nodeid):
    links = []
    records = []
    d = direction.capitalize()
    g = 'output/%s' % filename
    in_file = open(g, 'r')
    data = json.load(in_file)
    for x in data:
        if nodeid == x['NodeID']:
            for s in x['Links'][d]:
                if s not in links:
                    links.append(s)
    for l in links:
        for t in data:
            if l == t['NodeID']:
                rec = t['EntityType'], t['Data']
                if rec not in records:
                    records.append(rec)
    return render_template('popup-links.html', filename=filename, direction=d, nodeid=nodeid, records=records)


@app.errorhandler(404)
def not_found(error):
    e = 'Whoops, page not found!!!..try again'
    return render_template('404.html', error=e)


if __name__ == '__main__':
    app.run(debug=True)
