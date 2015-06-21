import os
from flask import Flask,render_template, redirect, url_for, request
import requests
import string

app = Flask(__name__)

@app.route('/')
def Welcome():
	return 'Welcome to my app running on Bluemix!'

@app.route('/index')
def index():
    



    ##image to text
    name = "spn7.PNG"
    image = open('images/'+name,'rb')
    url="http://api.idolondemand.com/1/api/sync/ocrdocument/v1"
    apikey="9e791393-6bc4-461f-a0f1-58c3203b64b1"
    def postrequests(function,data={},files={}):
               data["apikey"]=apikey
               callurl=url.format(function)
               r=requests.post(callurl,data=data,files=files)
               return r.json()

    result=postrequests('ocrdocument',data={},files={'file': image})
    text =  result[u'text_block']
    text = text[0]
    text = text[u'text']

    

    ##language recognition
    url = "https://gateway.watsonplatform.net/language-identification-beta/api"
    username = "557a7074-4492-4237-9ee5-c0e1a334411f"
    password = "aYga0TFTOvPP"
    data = { 'txt': text, 'sid': "lid-generic" }
  
    response=requests.post(url,auth=(username, password),data=data)
    
    orig = response.content[0:2]+response.content[3:5]
    orig = orig.lower()

	##language translation
    url = "https://gateway.watsonplatform.net/machine-translation-beta/api"
    mysid = "mt-"+orig+"-enus"
    username = "aa600dc3-7ad3-41a4-b742-fc70bf92d086"
    password = "qhQudzTHwSqW"
    data = { 'txt': text, 'sid': mysid }
  
    response=requests.post(url,auth=(username, password),data=data)
    text = response.content

    print text

    #text to speech
    url = "https://stream.watsonplatform.net/text-to-speech-beta/api/v1/synthesize"
    username = "561b8feb-f481-4fa1-bd28-8de0e41fdeb0"
    password = "9bfsBYCbL2aM"
    data = { 'voice': "VoiceEnUsMichael", 'text': text}
    response = None 
    while not response:
    	response=requests.get(url,auth=(username, password),params=data, headers={ 'accept': "audio/wav"}, stream=True, verify=False)
    name = "myfile.wav"
    
    os.remove("static/music/"+name)

    temp = raw_input()
    print temp

    file = open("static/music/"+name,"w")
    file.write(response.content)
    file.close()

    return render_template('index.html',music=name,text=text)


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
