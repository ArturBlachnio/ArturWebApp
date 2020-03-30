from flask import Blueprint, render_template

main = Blueprint(name='main', import_name=__name__)


@main.route('/')
def home():
    return render_template('home.html')
