from ibudget import app
from flask import render_template


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ibudget')
def ibudget():
    return render_template('ibudget.html')
