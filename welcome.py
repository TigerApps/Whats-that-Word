import os
from flask import Flask,render_template, redirect, url_for, request
import requests
import string
from werkzeug import secure_filename

app = Flask(__name__, static_folder='static', static_url_path='/static')

#UPLOAD_FOLDER = 'static/image/'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF', 'tiff', 'TIFF'])

#import cloudant

# connect to your account
# in this case, https://garbados.cloudant.com
# USERNAME = "ca2a2ff1-a78d-453d-92f5-27dcdc18e536-bluemix"
# PASSWORD = "3e519b6329052878063c266488bd41d9377c047d3cd38b8d8cb61ffe5feb976a"
#account = cloudant.Account(USERNAME)
# login, so we can make changes
#login = account.login(USERNAME, PASSWORD)
#assert login.status_code == 200
# create a database object
#db = account.database('my')

#song = db.document('song_doc')

##routes
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/about', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    ##get file from user
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                print filename  
            except:
                pass
            name = filename
        
        ##image to text
        url="http://api.idolondemand.com/1/api/sync/ocrdocument/v1"
        apikey="9e791393-6bc4-461f-a0f1-58c3203b64b1"
        def postrequests(function,data={},files={}):
                   data["apikey"]=apikey
                   callurl=url.format(function)
                   r=requests.post(callurl,data=data,files=files)
                   return r.json()
        
        result = None 
        while not result:
            result=postrequests('ocrdocument',data={},files={'file': file})
        text =  result[u'text_block']
        text = text[0]
        text = text[u'text']
        try:
            print text  
        except:
            pass
        ##language recognition
        url = "https://gateway.watsonplatform.net/language-identification-beta/api"
        username = "557a7074-4492-4237-9ee5-c0e1a334411f"
        password = "aYga0TFTOvPP"
        data = { 'txt': text, 'sid': "lid-generic" }
        response=requests.post(url,auth=(username, password),data=data)
        orig = response.content[0:2]+response.content[3:5]
        orig = orig.lower()
        try:
            print orig  
        except:
            pass
        
        ##language translation
        url = "https://gateway.watsonplatform.net/machine-translation-beta/api"
        mysid = "mt-"+orig+"-enus"
        username = "aa600dc3-7ad3-41a4-b742-fc70bf92d086"
        password = "qhQudzTHwSqW"
        data = { 'txt': text, 'sid': mysid }
      
        try:
            response=requests.post(url,auth=(username, password),data=data)
        except:
            return "couldnt"
        text = response.content
        try:
            print text  
        except:
            pass
        
        #text to speech
        url = "https://stream.watsonplatform.net/text-to-speech-beta/api/v1/synthesize"
        username = "561b8feb-f481-4fa1-bd28-8de0e41fdeb0"
        password = "9bfsBYCbL2aM"
        data = { 'voice': "VoiceEnUsMichael", 'text': text}
        response = None 
        while not response:
            response=requests.get(url,auth=(username, password),params=data, headers={ 'accept': "audio/wav"}, stream=True, verify=False)
        #name = "myfile.wav"
        name = text[:10]+".wav"
        file = open("static/music/"+name,"w")
        file.write(response.content)
        file.close()
        return render_template('index.html', text=text, music=name)
    return  render_template('home.html')


port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
