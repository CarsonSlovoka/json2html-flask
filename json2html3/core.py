import html

from flask import Flask
from flask import request
from flask import render_template as flask_renter_template

from .api.convertor import HTMLConvertor

from pathlib import Path

app = Flask(__name__,
            static_folder=str(Path(__file__).parent / Path('static')),
            template_folder=str(Path(__file__).parent / Path('templates')),
            )

app.config.update(
    dict(
        PAGE_SETTING=dict(
            github_url='https://github.com/CarsonSlovoka/json2html-flask',
            stackoverflow_url='https://stackoverflow.com/users/9935654/carson?tab=profile',
            disqus=dict(
                show=False,
                language='en',  # en, zh-TW
                disqus_short_name='json2html-1'
            ),
        )
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
    if checkbox == "1":
        style = "<table class=\"table table-condensed table-bordered table-hover\">"
    else:
        style = "<table border=\"1\">"

    try:
        conv = HTMLConvertor(text, style)
        return render_template("index.html", processed_text=html.unescape(conv.convert()), pro=text)
    except Exception as e:
        return render_template("index.html", error=f"Error Parsing JSON ! Please check your JSON syntax: {str(e)}", pro=text)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
