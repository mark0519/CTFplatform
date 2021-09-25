import hashlib
import json

from time import time
from urllib.parse import urlparse
from uuid import uuid4
from argparse import ArgumentParser

import requests

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
