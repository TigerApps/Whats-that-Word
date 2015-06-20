import os
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Read port selected by the cloud for our application
PORT = int(os.getenv('VCAP_APP_PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass

from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
from app import app
import requests

app = Flask(__name__)


@app.route('/')
def index():
    """Index Redirect Page"""
    image = open('phototest.tif','rb')
    url="http://api.idolondemand.com/1/api/sync/ocrdocument/v1"
    apikey="9e791393-6bc4-461f-a0f1-58c3203b64b1"

    def postrequests(function,data={},files={}):
               data["apikey"]=apikey
               callurl=url.format(function)
               r=requests.post(callurl,data=data,files=files)
               return r.json()

    result=postrequests('ocrdocument',data={'mode':'photo'},files={'file': image})
    text =  result[u'text_block']
    text = text[0]
    text = text[u'text']

    return render_template('index2.html',show=text)



@app.errorhandler(404)
def page_not_found(error):
    """redirect wrong urls to inxed"""
    return redirect(url_for('index'))





