from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

