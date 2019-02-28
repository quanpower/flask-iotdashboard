"""A separate Flask app that serves fake endpoints for demo purposes."""

# -*- coding: utf-8 -*-

from itertools import combinations
import json
import locale
import os
from datetime import timedelta as td
from datetime import datetime as dt
from random import randrange as rr
from random import choice, random
import time

from flask import (
    Flask,
    abort,
    request,
    jsonify,
    render_template,
    flash,
)
from flask_cors import CORS
from flask_cors import cross_origin


from flask_sqlalchemy import SQLAlchemy


app = Flask('endpoints_test')
CORS(app)
app.config['SECRET_KEY'] = 'NOTSECURELOL'
app.debug = True

STRESS_MAX_POINTS = 300

locale.setlocale(locale.LC_ALL, '')

cwd = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daq.db'
db = SQLAlchemy(app)



class DAQS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(80), unique=True)
    daq_value = db.Column(db.Float, unique=True)
    daq_time = db.Column(db.INTEGER)

    def __repr__(self):
        return '<DAQS %r>' % self.id


def recursive_d3_data(current=0, max_iters=12, data=None):
    """Generate d3js data for stress testing.
    Format is suitable in treemap, circlepack and dendrogram testing.
    """
    if current >= max_iters:
        return data
    if data is None:
        data = dict(name='foo', size=rr(10, 10000), children=[])
    data = dict(name='foo', size=rr(10, 10000),
                children=[data, data])
    return recursive_d3_data(
        current=current + 1,
        max_iters=max_iters,
        data=data)


def dates_list(max_dates=10):
    """Generate a timeseries dates list."""
    now = dt.now()
    return [str(now + td(days=i * 10))[0:10] for i in range(max_dates)]


def rr_list(max_range=10):
    """Generate a list of random integers."""
    return [rr(0, 100) for i in range(max_range)]


def rand_hex_color():
    """Generate a random hex color.
    e.g. #FF0000
    """
    chars = list('0123456789ABCDEF')
    return '#{0}{1}{2}{3}{4}{5}'.format(
        choice(chars),
        choice(chars),
        choice(chars),
        choice(chars),
        choice(chars),
        choice(chars),
    )


@cross_origin()
@app.route('/numbergroup')
def numbergroup():
    """Fake endpoint."""
    dataset = int(request.args.get('dataset', 0))
    # multiple examples shown here for variadic demonstrations
    datas = [
        [
            {
                "title": "油箱液位",
                "description": 'mm',
                "data": 32.51,
                "color": "green",
            },
            {
                "title": "1#坑道液位",
                "description": 'mm',
                "data": 74.5,
                "color": "red",

            },
            {
                "title": "2#坑道液位",
                "description": "mm",
                "data": 54.12,
                "color": "green",
            },
            {
                "title": "3#坑道液位",
                "description": "mm",
                "data": 12.34,
                "color": "green",
            },
        ],
        [
            {
                "title": "Simple thing",
                "data": 2,
                "width": "33%",
                "description": "Just a simple number"
            },
            {
                "title": "Simple thing 2",
                "data": 4033,
                "width": "33%",
                "description": "Just a simple number"
            },
            {
                "title": "Simple thing 3",
                "data": 49102,
                "width": "33%",
                "description": "Just a simple number"
            },
        ],
        [
            {
                "title": "Average time on site",
                "description": "Signed in to signed out (units nostyle)",
                "data": '20 minutes',
                "color": "#7D4EE4",
            },
            {
                "title": "Average time on site page X",
                "description": "Signed in to signed out (custom units style)",
                "data": 15,
                "units": "minutes",
            },
            {
                "title": "Average $ spent per day",
                "description": "Yeeehaw (custom units style)",
                "data": 130,
                "units": "dollars"
            },
        ]
    ]
    return jsonify(datas[dataset])


@cross_origin()
@app.route('/combination')
def combination():
    """Fake endpoint."""
    data = {
        'columns': [
            ['data1', 30, 20, 50, 40, 60, 50],
            ['data2', 200, 130, 90, 240, 130, 220],
            ['data3', 300, 200, 160, 400, 250, 250],
            ['data4', 200, 130, 90, 240, 130, 220],
            ['data5', 130, 120, 150, 140, 160, 150],
            ['data6', 90, 70, 20, 50, 60, 120],
        ],
        'type': 'bar',
        'types': {
            'data3': 'spline',
            'data4': 'line',
            'data6': 'area',
        },
        'groups': [
            ['data1', 'data2'],
        ]
    }
    return jsonify(dict(data=data))


@cross_origin()
@app.route('/timeseriesc3')
def timeseriesc3():
    """Fake endpoint."""
    return jsonify(dict(
        dates=[
            '19{}-{}-{}'.format(rr(10, 99), rr(10, 31), rr(10, 31))
            for _ in range(4)
        ],
        abc=rr_list(max_range=4),
        cde=rr_list(max_range=4),
    ))


@cross_origin()
@app.route('/stacked-bar')
def stackedbar():
    """Fake endpoint."""
    return jsonify({
        'data': {
            'columns': [
                ['data1', -30, 200, 200, 400, -150, 250],
                ['data2', 130, 100, -100, 200, -150, 50],
                ['data3', -230, 200, 200, -300, 250, 250]
            ],
            'type': 'bar',
            'groups': [
                ['data1', 'data2']
            ]
        },
        'grid': {
            'y': {
                'lines': [{'value': 0}]
            }
        }
    })


@cross_origin()
@app.route('/wordcloud')
def wordcloud():
    """Fake endpoint."""
    words = [
        'awesome', 'rad', 'neato', 'the', 'flask', 'jsondash', 'graphs',
        'charts', 'd3', 'js', 'dashboards', 'c3',
    ]
    sizes = range(len(words))
    data = [
        {
            'text': word,
            'size': sizes[i] * 12
        }
        for i, word in enumerate(words)
    ]
    return jsonify(data)


@cross_origin()
@app.route('/sigma')
def sigma():
    """Fake endpoint."""
    chart_name = request.args.get('name', 'basic')
    if chart_name == 'random':
        nodes = request.args.get('nodes', 'abcdefghij')
        _vertices = list(nodes)
        _edges = combinations(_vertices, 2)
        edges, vertices = [], []
        for (frm, to) in _edges:
            edges.append(dict(
                id='{}-{}'.format(frm, to),
                color=rand_hex_color(),
                source=frm,
                target=to,
                size=rr(1, 10),
                x=rr(1, 100),
                y=rr(1, 100),
            ))
        for vertex in _vertices:
            vertices.append(dict(
                id=vertex,
                size=rr(1, 10),
                x=rr(1, 100),
                y=rr(1, 100),
                color=rand_hex_color(),
                label='node {}'.format(vertex),
            ))
        data = dict(
            nodes=vertices,
            edges=edges,
        )
        return jsonify(data)
    filename = '{}/examples/sigma/{}.json'.format(cwd, chart_name)
    try:
        with open(filename, 'r') as chartjson:
            return chartjson.read()
    except IOError:
        pass
    return jsonify({})


@cross_origin()
@app.route('/flamegraph')
def flamegraph():
    """Fake endpoint."""
    chart_name = request.args.get('name', 'stacks')
    filename = '{}/examples/flamegraph/{}.json'.format(cwd, chart_name)
    try:
        with open(filename, 'r') as chartjson:
            return chartjson.read()
    except IOError:
        pass
    return jsonify({})


@cross_origin()
@app.route('/cytoscape')
def cytoscape():
    """Fake endpoint.

    Reads data from a local cytoscape spec, and if there is a
    remote url specified, (assuming it exists here), open and load it as well.

    This returns all required json as a single endpoint.
    """
    chart_name = request.args.get('name', 'basic')
    filename = '{}/examples/cytoscape/{}.json'.format(cwd, chart_name)
    try:
        with open(filename, 'r') as chartjson:
            return chartjson.read()
    except IOError:
        pass
    return jsonify({})


@cross_origin()
@app.route('/vegalite')
def vegalite():
    """Fake endpoint.

    Reads data from a local vega spec, and if there is a
    remote url specified, (assuming it exists here), open and load it as well.

    This returns all required json as a single endpoint.
    """
    chart_type = request.args.get('type', 'bar')
    filename = '{}/examples/vegalite/{}.json'.format(cwd, chart_type)
    try:
        with open(filename, 'r') as chartjson:
            chartjson = chartjson.read()
            data = json.loads(chartjson)
            if data.get('data', {}).get('url') is not None:
                datapath = '{}/examples/vegalite/{}'.format(
                    cwd, data['data']['url']
                )
                with open(datapath, 'r') as datafile:
                    if datapath.endswith('.json'):
                        raw_data = datafile.read()
                        raw_data = json.loads(raw_data)
                    # TODO: adding csv support for example.
                    data.update(data=dict(
                        name='some data',
                        values=raw_data,
                    ))
                    return jsonify(data)
            else:
                return chartjson
    except IOError:
        pass
    return jsonify({})


@cross_origin()
@app.route('/plotly')
def plotly():
    """Fake endpoint."""
    chart_type = request.args.get('chart', 'line')
    filename = '{}/examples/plotly/{}.json'.format(cwd, chart_type)
    with open(filename, 'r') as chartjson:
        return chartjson.read()
    return jsonify({})


@cross_origin
@app.route('/plotly-dynamic')
def plotly_dynamic():
    """Fake endpoint."""
    filename = '{}/examples/plotly/bar_line_dynamic.json'.format(cwd)
    with open(filename, 'r') as chartjson:
        return chartjson.read()
    return jsonify({})


@cross_origin()
@app.route('/timeline')
def timeline():
    """Fake endpoint."""
    with open('{}/examples/timeline3.json'.format(cwd), 'r') as timelinejson:
        return timelinejson.read()
    return jsonify({})


@app.route('/dtable', methods=['GET'])
def dtable():
    """Fake endpoint."""
    if 'stress' in request.args:
        return jsonify([
            dict(
                foo=rr(1, 1000),
                bar=rr(1, 1000),
                baz=rr(1, 1000),
                quux=rr(1, 1000)) for _ in range(STRESS_MAX_POINTS)
        ])
    fname = 'dtable-override' if 'override' in request.args else 'dtable'
    with open('{}/examples/{}.json'.format(os.getcwd(), fname), 'r') as djson:
        return djson.read()
    return jsonify({})


@cross_origin()
@app.route('/timeseries')
def timeseries():
    """Fake endpoint."""
    return jsonify({
        "dates": dates_list(),
        "line1": rr_list(max_range=10),
        "line2": rr_list(max_range=10),
        "line3": rr_list(max_range=10),
    })


@cross_origin()
@app.route('/custom')
def custompage():
    """Fake endpoint."""
    kwargs = dict(number=rr(1, 1000))
    return render_template('examples/custom.html', **kwargs)



@cross_origin()
@app.route('/gauge')
def gauge():
    """Fake endpoint."""
    return jsonify({'data': rr(1, 100)})


@cross_origin()
@app.route('/area-custom')
def area_custom():
    """Fake endpoint."""
    return jsonify({
        "data": {
            "columns": [
                ["data1", 300, 350, 300, 0, 0, 0],
                ["data2", 130, 100, 140, 200, 150, 50]
            ],
            "types": {
                "data1": "area",
                "data2": "area-spline"
            }
        }
    })


@cross_origin()
@app.route('/scatter')
def scatter():
    """Fake endpoint."""
    if 'override' in request.args:
        with open('{}/examples/overrides.json'.format(cwd), 'r') as jsonfile:
            return jsonfile.read()
    return jsonify({
        "bar1": [1, 2, 30, 12, 100],
        "bar2": rr_list(max_range=40),
        "bar3": rr_list(max_range=40),
        "bar4": [-10, 1, 5, 4, 10, 20],
    })


@cross_origin()
@app.route('/pie')
def pie():
    """Fake endpoint."""
    letters = list('abcde')
    if 'stress' in request.args:
        letters = range(STRESS_MAX_POINTS)
    return jsonify({'data {}'.format(name): rr(1, 100) for name in letters})


@cross_origin()
@app.route('/custom-inputs')
def custom_inputs():
    """Fake endpoint."""
    _range = int(request.args.get('range', 5))
    entries = int(request.args.get('entries', 3))
    starting = int(request.args.get('starting_num', 0))
    prefix = request.args.get('prefix', 'item')
    if 'override' in request.args:
        show_axes = request.args.get('show_axes', False)
        show_axes = show_axes == 'on'
        data = dict(
            data=dict(
                columns=[
                    ['{} {}'.format(prefix, i)] + rr_list(max_range=entries)
                    for i in range(starting, _range)
                ],
            )
        )
        if show_axes:
            data.update(axis=dict(
                x=dict(label='This is the X axis'),
                y=dict(label='This is the Y axis')))
        return jsonify(data)
    return jsonify({
        i: rr_list(max_range=_range) for i in range(starting, entries)
    })


@cross_origin()
@app.route('/bar')
def barchart():
    """Fake endpoint."""
    if 'stress' in request.args:
        return jsonify({
            'bar-{}'.format(k): rr_list(max_range=STRESS_MAX_POINTS)
            for k in range(STRESS_MAX_POINTS)
        })
    return jsonify({
        "bar1": [1, 2, 30, 12, 100],
        "bar2": rr_list(max_range=5),
        "bar3": rr_list(max_range=5),
    })


@cross_origin()
@app.route('/line')
def linechart():
    """Fake endpoint."""
    if 'stress' in request.args:
        return jsonify({
            'bar-{}'.format(k): rr_list(max_range=STRESS_MAX_POINTS)
            for k in range(STRESS_MAX_POINTS)
        })
    return jsonify({
        "line1": [1, 4, 3, 10, 12, 14, 18, 10],
        "line2": [1, 2, 10, 20, 30, 6, 10, 12, 18, 2],
        "line3": rr_list(),
    })


@cross_origin()
@app.route('/shared')
def shared_data():
    """Fake endpoint to demonstrate sharing data from one source."""
    letters = list('abcde')
    piedata = {'data {}'.format(name): rr(1, 100) for name in letters}
    bardata = {
        "bar1": [1, 2, 30, 12, 100],
        "bar2": rr_list(max_range=5),
        "bar3": rr_list(max_range=5),
    }
    linedata = {
        "line1": [1, 4, 3, 10, 12, 14, 18, 10],
        "line2": [1, 2, 10, 20, 30, 6, 10, 12, 18, 2],
        "line3": rr_list(),
    }
    return jsonify({
        'multicharts': {
            'line': linedata,
            'bar': bardata,
            'pie': piedata,
        }
    })


@cross_origin()
@app.route('/singlenum')
def singlenum():
    """Fake endpoint."""
    _min, _max = 10, 10000
    if 'sales' in request.args:
        val = locale.currency(float(rr(_min, _max)), grouping=True)
    else:
        val = rr(_min, _max)
    if 'negative' in request.args:
        val = '-{}'.format(val)
    return jsonify(data=val)


@cross_origin()
@app.route('/deadend')
def test_die():
    """Fake endpoint that ends in a random 50x error."""
    # Simulate slow connection
    sleep = request.args.get('sleep', True)
    if sleep != '':
        sleep_for = request.args.get('sleep_for')
        time.sleep(int(sleep_for) if sleep_for is not None else random())
    err_code = request.args.get('error_code')
    rand_err = choice([500, 501, 502, 503, 504])
    abort(int(err_code) if err_code is not None else rand_err)


@cross_origin()
@app.route('/venn')
def test_venn():
    """Fake endpoint."""
    data = [
        {'sets': ['A'], 'size': rr(10, 100)},
        {'sets': ['B'], 'size': rr(10, 100)},
        {'sets': ['C'], 'size': rr(10, 100)},
        {'sets': ['A', 'B'], 'size': rr(10, 100)},
        {'sets': ['A', 'B', 'C'], 'size': rr(10, 100)},
    ]
    return jsonify(data)


@cross_origin()
@app.route('/sparklines', methods=['GET'])
def sparklines():
    """Fake endpoint."""
    if any([
        'pie' in request.args,
        'discrete' in request.args,
    ]):
        return jsonify([rr(1, 100) for _ in range(10)])
    return jsonify([[i, rr(i, 100)] for i in range(10)])


@cross_origin()
@app.route('/circlepack', methods=['GET'])
def circlepack():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return jsonify(recursive_d3_data())
    with open('{}/examples/flare.json'.format(cwd), 'r') as djson:
        return djson.read()
    return jsonify({})


@cross_origin()
@app.route('/treemap', methods=['GET'])
def treemap():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return jsonify(recursive_d3_data())
    with open('{}/examples/flare.json'.format(cwd), 'r') as djson:
        return djson.read()
    return jsonify({})


@cross_origin()
@app.route('/map', methods=['GET'])
def datamap():
    """Fake endpoint."""
    return render_template('examples/map.html')


@cross_origin()
@app.route('/dendrogram', methods=['GET'])
def dendro():
    """Fake endpoint."""
    if 'stress' in request.args:
        # Build a very large dataset
        return jsonify(recursive_d3_data())
    filename = 'flare-simple' if 'simple' in request.args else 'flare'
    with open('{}/examples/{}.json'.format(cwd, filename), 'r') as djson:
        return djson.read()
    return jsonify({})


@cross_origin()
@app.route('/voronoi', methods=['GET'])
def voronoi():
    """Fake endpoint."""
    w, h = request.args.get('width', 800), request.args.get('height', 800)
    max_points = int(request.args.get('points', 100))
    if 'stress' in request.args:
        max_points = 500
    return jsonify([[rr(1, h), rr(1, w)] for _ in range(max_points)])


@cross_origin()
@app.route('/digraph', methods=['GET'])
def graphdata():
    """Fake endpoint."""
    if 'filetree' in request.args:
        with open('{}/examples/filetree_digraph.dot'.format(cwd), 'r') as dot:
            return jsonify(dict(graph=dot.read()))
    if 'simple' in request.args:
        graphdata = """
        digraph {
            a -> b;
            a -> c;
            b -> c;
            b -> a;
            b -> b;
        }
        """
        return jsonify(dict(graph=graphdata))
    nodes = list('abcdefghijkl')
    node_data = '\n'.join([
        '{0} -> {1};'.format(choice(nodes), choice(nodes))
        for _ in range(10)
    ])
    graphdata = """digraph {lb} {nodes} {rb}""".format(
        lb='{', rb='}', nodes=node_data)
    return jsonify(dict(
        graph=graphdata,
    ))

@cross_origin()
@app.route('/channel/<channel_id>')
def channel(channel_id):
    value = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).first()

    return jsonify(value=value.daq_value)



@cross_origin()
@app.route('/daq_value/<channel_id>')
def daq_value(channel_id):

    return render_template('examples/daq_value.html',channel_id=channel_id)



@cross_origin()
@app.route('/oil_temperature/<channel_id>')
def oil_temperature(channel_id):
    """Fake endpoint."""
    temperature = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).first()
    return render_template('examples/oil_temperature.html',channel_id=channel_id)


@cross_origin()
@app.route('/oil_level/<channel_id>')
def oil_level(channel_id):
    level = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).first()

    return render_template('examples/oil_level.html',channel_id=channel_id)


@cross_origin()
@app.route('/water_level/<channel_id>')
def water_level(channel_id):
    level = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).first()
    flash('water_level error', 'error')
    return render_template('examples/water_level.html',channel_id=channel_id)


@cross_origin()
@app.route('/h5video/<video_id>')
def h5video(video_id):

    return render_template('examples/h5video.html',video_id=video_id)


@cross_origin()
@app.route('/h5video2/')
def h5video2():

    return render_template('examples/h5video2.html')


@cross_origin()
@app.route('/h5video3/')
def h5video3():

    return render_template('examples/h5video3.html')



@cross_origin()
@app.route('/channel_history/<channel_id>')
def channel_history(channel_id):
    """Fake endpoint."""

    all_channels = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).limit(50).all()

    channel_list = []
    for channel in all_channels:
        value = channel.daq_value
        channel_list.append(value)
        channel_list.reverse()


    return jsonify(channel_list)



@cross_origin()
@app.route('/history_line')
def history_line():
    """Fake endpoint."""
    return render_template('examples/history_line.html')


@cross_origin()
@app.route('/daq_history_line')
def daq_history_line():
    """Fake endpoint."""
    return_list = []
    line_name = ['line0','oil_temperature','oil_level','water_level']
    for channel_id in range(1,8):
        all_channels = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).limit(50).all()

        channel_list = []
        for channel in all_channels:
            value = channel.daq_value
            channel_list.append(value)
            channel_list.reverse()


        return_list.append({"data":channel_list})
    print(return_list)

    return jsonify(return_list)


@cross_origin()
@app.route('/history_record')
def history_record():
    """Fake endpoint."""

    return render_template('examples/history_record.html')



@cross_origin()
@app.route('/daq_history_record')
def daq_history_record():
    """Fake endpoint."""

    all_channels = DAQS.query.order_by(-DAQS.daq_time).limit(2000).all()

    print(all_channels)
    channel_list = []
    for channel in all_channels:
        print(channel.daq_time)
        channel_list.append({
            'id':channel.id,
            'channel_id':channel.channel_id,
            'channel_name':channel.channel_id,
            'daq_value':channel.daq_value,
            'daq_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(channel.daq_time))
            })
        
    print(channel_list)

    return jsonify(channel_list)



@cross_origin()
@app.route('/waring')
def waring():
    """Fake endpoint."""
    value_1 = DAQS.query.filter_by(channel_id=1).order_by(-DAQS.daq_time).first()

    value_2 = DAQS.query.filter_by(channel_id=2).order_by(-DAQS.daq_time).first()
    print(value_2)
    print(value_2.daq_value)

    value_3 = DAQS.query.filter_by(channel_id=3).order_by(-DAQS.daq_time).first()
    value_4 = DAQS.query.filter_by(channel_id=4).order_by(-DAQS.daq_time).first()
    value_5 = DAQS.query.filter_by(channel_id=5).order_by(-DAQS.daq_time).first()
    value_6 = DAQS.query.filter_by(channel_id=6).order_by(-DAQS.daq_time).first()
    value_7 = DAQS.query.filter_by(channel_id=7).order_by(-DAQS.daq_time).first()


    if value_2.daq_value > 800:
        return_dict = {"message":"警告: 350T环轧机油箱液位高于上限!    Warning: oil level  > high limit!", "catgory":"error", "status":1}
    elif value_2.daq_value < 600:
        return_dict = {"message":"警告: 350T环轧机油箱液位低于下限!    Warning: oil level  < low limit!", "catgory":"error", "status":1}
    else:
        return_dict = {"message":"", "catgory":"error", "status":0}
    
    if value_5.daq_value > 800:
        return_dict1 = {"message":"警告: 3000T压机油箱液位高于上限!    Warning: oil level  > high limit!", "catgory":"error", "status":1}
    elif value_5.daq_value < 600:
        return_dict1 = {"message":"警告: 3000T压机油箱液位低于下限!    Warning: oil level  < low limit!", "catgory":"error", "status":1}
    else:
        return_dict1 = {"message":"", "catgory":"error", "status":0}
    

    # print(return_dict)
    # return_dict = {"message":"alarm error", "catgory":"error", "status":1}
    return jsonify([return_dict, return_dict1])


@cross_origin()
@app.route('/hole')
def hole():

    return render_template('examples/hole.html')


@cross_origin()
@app.route('/oil')
def oil():
    # level = DAQS.query.filter_by(channel_id=channel_id).order_by(-DAQS.daq_time).first()

    return render_template('examples/oil.html')


@cross_origin()
@app.route('/localtime')
def localtime():

    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))



if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5004))
    HOST = os.getenv('HOST', '0.0.0.0')
    app.run(debug=True, host=HOST, port=PORT)
