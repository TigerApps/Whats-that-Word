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
    # image = open('right.jpg','rb')
    # url="http://api.idolondemand.com/1/api/sync/ocrdocument/v1"
    # apikey="9e791393-6bc4-461f-a0f1-58c3203b64b1"
	# def postrequests(function,data={},files={}):
    #            data["apikey"]=apikey
    #            callurl=url.format(function)
    #            r=requests.post(callurl,data=data,files=files)
    #            return r.json()

    # result=postrequests('ocrdocument',data={},files={'file': image})
    # text =  result[u'text_block']
    # text = text[0]
    # text = text[u'text']

    text = "derecho es mi casa"

    ##language recognition
    url = "https://gateway.watsonplatform.net/language-identification-beta/api"
    username = "557a7074-4492-4237-9ee5-c0e1a334411f"
    password = "aYga0TFTOvPP"
    data = { 'txt': text, 'sid': "lid-generic" }
  
    response=requests.post(url,auth=(username, password),data=data)
    
    orig = response.content[0:2]+response.content[3:5]
    orig = orig.lower()

	#language translation
    url = "https://gateway.watsonplatform.net/machine-translation-beta/api"
    mysid = "mt-"+orig+"-enus"
    username = "aa600dc3-7ad3-41a4-b742-fc70bf92d086"
    password = "qhQudzTHwSqW"
    data = { 'txt': text, 'sid': mysid }
  
    response=requests.post(url,auth=(username, password),data=data)
    text = response.content

    print text
    #text = "hello"
    #text to speech
    url = "https://stream.watsonplatform.net/text-to-speech-beta/api/v1/synthesize"
    username = "561b8feb-f481-4fa1-bd28-8de0e41fdeb0"
    password = "9bfsBYCbL2aM"
    data = { 'voice': "VoiceEnUsMichael", 'text': text} #, 'headers': {'x-logging': '0'}}
    # , 'X-logging': '0' }
    #data = { 'accept': 'audio/wav', 'voice': 'VoiceEnUsMichael', 'text':text} #, 'X-logging': '0' }

    #response=requests.head(url,auth=(username, password)) #,params=data)
    response=requests.get(url,auth=(username, password),params=data, headers={ 'accept': "audio/wav"}, stream=True, verify=False)
    #print response
    text = response.content
    #print text
    name = "myfile.wav"
    file = open(name,"wb")
    file.write(text)
    file.close()

    file = open("response.txt","w")
    file.write(str(response))
    file.close()

    file = open("content.txt","w")
    file.write(text)
    file.close()

    #name = "\""+name+"\""
    return render_template('index2.html',show=name)




# {
#   "language_identification": [
#     {
#       "name": "Language Identification-9r",
#       "label": "language_identification",
#       "plan": "language_identification_free_plan",
#       "credentials": {
#         "url": "https://gateway.watsonplatform.net/language-identification-beta/api",
#         "sids": [
#           {
#             "sid": "lid-generic",
#             "description": "language identification of any text"
#           }
#         ],
#         "username": "557a7074-4492-4237-9ee5-c0e1a334411f",
#         "password": "aYga0TFTOvPP"
#       }
#     }
#   ]
# }

# {
#   "machine_translation": [
#     {
#       "name": "Machine Translation-li",
#       "label": "machine_translation",
#       "plan": "machine_translation_free_plan",
#       "credentials": {
#         "url": "https://gateway.watsonplatform.net/machine-translation-beta/api",
#         "sids": [
#           {
#             "sid": "mt-ptbr-enus",
#             "description": "translation from Portuguese to English"
#           },
#           {
#             "sid": "mt-enus-ptbr",
#             "description": "translation from English to Portuguese"
#           },
#           {
#             "sid": "mt-enus-eses",
#             "description": "translation from English to Spanish"
#           },
#           {
#             "sid": "mt-eses-enus",
#             "description": "translation from Spanish to English"
#           },
#           {
#             "sid": "mt-frfr-enus",
#             "description": "translation from French to English"
#           },
#           {
#             "sid": "mt-enus-frfr",
#             "description": "translation from English to French"
#           },
#           {
#             "sid": "mt-arar-enus",
#             "description": "translation from Arabic to English"
#           },
#           {
#             "sid": "mt-enus-arar",
#             "description": "translation from English to Arabic"
#           }
#         ],
#         "username": "aa600dc3-7ad3-41a4-b742-fc70bf92d086",
#         "password": "qhQudzTHwSqW"
#       }
#     }
#   ]
# }

# {
#   "text_to_speech": [
#     {
#       "name": "Text to Speech-4c",
#       "label": "text_to_speech",
#       "plan": "free",
#       "credentials": {
#         "url": "https://stream.watsonplatform.net/text-to-speech-beta/api",
#         "username": "561b8feb-f481-4fa1-bd28-8de0e41fdeb0",
#         "password": "9bfsBYCbL2aM"
#       }
#     }
#   ]
# }


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)