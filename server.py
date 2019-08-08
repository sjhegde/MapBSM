from flask import Flask
import flask
import BSMVisBackend
app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World!'

@app.route('/geojson')
def geojson():
    response = flask.Response(BSMVisBackend.currentCars())
    response.headers['Content-Type'] = 'text/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    return response
