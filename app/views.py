"""
Rec-Sys is a login based database system implementing the recommendation system
for searching of Documents
"""

# all the imports
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm



import requests

# @lm.user_loader
# def load_user(id):
#     """Given *user_id*, return the associated User object.
#     :param unicode user_id: user_id (username) user to retrieve
#     """
#     return User.query.get(int(id))

# @app.before_request
# def before_request():
#     g.user = current_user


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

    return render_template('index.html',show=text)



@app.errorhandler(404)
def page_not_found(error):
    """redirect wrong urls to login or database"""
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

