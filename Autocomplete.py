
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Returned(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    prefix = db.Column(db.String(32))

@app.route('/_autocomplete')
def autocomplete():


    """Add two numbers server side, ridiculous but well..."""
    artists = ["Abba", "Bob Dylan", "Bobby McFerren", "Billy Joel", "Billie Holiday"]
    text = request.args.get('q', "")

    matches = list()
    for a in artists:
        if a.lower().startswith(text.lower()):
            matches.append(a)

    return jsonify(result=matches)

@app.route('/_test')
def jsontest():
    # open file and read in lines
    with open('subjects.txt') as f:
        subjects = f.readlines()

    # strip all new line characters
    subjects = [x.strip() for x in subjects]

    subs = list()
    # info ={"courses":[]}
    for s in subjects:
        subs.append(s.split(","))

    return jsonify(subjects=subs)

@app.route('/_process', methods=['GET','POST'])
def process():
    if request.method == 'POST':
        res = request.json
        for r in res:
          db.session.add(Returned(level=r.split("-")[1], prefix=r.split("-")[0]))
        db.session.commit()
        # return redirect(url_for('result'))

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('tests.html')

@app.route('/result')
def result():
    info = Returned.query.all()
    return render_template('result.html', info=info)

if __name__ == '__main__':
    app.run(port=5003)