from flask import Blueprint, render_template

ibudget = Blueprint(name='ibudget', import_name=__name__)


@ibudget.route('/ibudget')
def home():
    return render_template('ibudget/home.html')
