from flask import Flask

app = Flask(__name__)

from ibudget import routes
