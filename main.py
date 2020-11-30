"""
JSON 2 HTML convertor
=====================

(c) Varun Malhotra 2013
http://softvar.github.io

Source Code: https://github.com/softvar/json2html-flask
------------

LICENSE: MIT
--------
"""
# -*- coding: utf-8 -*-

# import ordereddict
# import HTMLParser
from collections import OrderedDict
from html.parser import HTMLParser
import html

from flask import json
from flask import Flask
from flask import request
from flask import render_template as flask_renter_template

from pathlib import Path

app = Flask(__name__,
            static_folder=str(Path(__file__).parent / Path('static')),
            template_folder=str(Path(__file__).parent / Path('templates')),
            )

a = ''

app.config.update(
    dict(
        PAGE_SETTING=
        dict(github_url='https://github.com/CarsonSlovoka/json2html-flask',
             stackoverflow_url='https://stackoverflow.com/users/9935654/carson?tab=profile',
             display_disqus=False,
             disqus_short_name='json2html-1')
    ))


def render_template(*args, **kwargs):
    kwargs.update(app.config['PAGE_SETTING'])
    return flask_renter_template(*args, **kwargs)


@app.route('/')
def my_form():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def my_form_post():
    """
    receive submitted data and process
    """
    text = request.form['text']
    checkbox = request.form['users']
    style = ""
    if checkbox == "1":
        style = "<table class=\"table table-condensed table-bordered table-hover\">"
    else:
        style = "<table border=\"1\">"

    # json_input = json.dumps(text)
    try:
        ordered_json = json.loads(text, object_pairs_hook=OrderedDict)
        print(ordered_json)
        processed_text = html_convertor(ordered_json, style)

        html_parser = HTMLParser()
        global a
        a = ''
        return render_template("index.html", processed_text=html.unescape(processed_text), pro=text)
    except Exception as e:
        return render_template("index.html", error=f"Error Parsing JSON ! Please check your JSON syntax: {str(e)}", pro=text)


def iter_json(ordered_json, style):
    global a
    a = a + style
    for k, v in ordered_json.items():
        a = a + '<tr>'
        a = a + '<th>' + str(k) + '</th>'
        if v is None:
            v = str("")
        if isinstance(v, list):
            a = a + '<td><ul>'
            for i in range(0, len(v)):
                if isinstance(v[i], str):
                    a = a + '<li>' + str(v[i]) + '</li>'
                elif isinstance(v[i], int) or isinstance(v[i], float):
                    a = a + '<li>' + str(v[i]) + '</li>'
                elif not isinstance(v[i], list):
                    iter_json(v[i], style)
            a = a + '</ul></td>'
            a = a + '</tr>'
        elif isinstance(v, str):
            a = a + '<td>' + str(v) + '</td>'
            a = a + '</tr>'
        elif isinstance(v, int) or isinstance(v, float):
            a = a + '<td>' + str(v) + '</td>'
            a = a + '</tr>'
        else:
            a = a + '<td>'
            # a=a+ '<table border="1">'
            iter_json(v, style)
            a = a + '</td></tr>'
    a = a + '</table>'


def html_convertor(ordered_json, style):
    """
    converts JSON Object into human readable HTML representation
    generating HTML table code with raw/bootstrap styling.
    """
    global a
    try:
        for k, v in ordered_json.items():
            pass
        iter_json(ordered_json, style)

    except Exception as e:
        for idx, val in enumerate(ordered_json):
            if isinstance(val, str):
                a = a + '<li>' + str(val) + '</li>'
            elif isinstance(val, int) or isinstance(val, float):
                a = a + '<li>' + str(val) + '</li>'
            elif not isinstance(val, list):
                html_convertor(val, style)

    return a


if __name__ == '__main__':
    app.run(debug=True)
