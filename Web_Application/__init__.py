from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# for text file upload
app.config['UPLOAD_FOLDER'] = "Web_Application/uploaded_files/"
app.config['MAX_CONTENT_PATH'] = 1000000  # max Mb
app.config['MAX_OUTLEN'] = 500  # max Mb


# For database managment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from Web_Application import routes