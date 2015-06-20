import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def Welcome():
	return 'Welcome to my app running on Bluemix!'

@app.route('/index')
def index():
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


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))