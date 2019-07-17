import time
import os

time.sleep(20)

from flask import Flask, request, render_template, send_from_directory, url_for
import sys
from flask_material import Material
from utils import *


app = Flask(__name__)
Material(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False, host= '0.0.0.0')