from flask import Flask


app = Flask(__name__)
app.config.from_object('config')


# intentionally imported at last
from app import views
