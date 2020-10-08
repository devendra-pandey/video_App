from flask import Flask , jsonify, make_response, render_template, flash, redirect, url_for, session, logging, request
import os


app = Flask(__name__, static_url_path='/static')


UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(__name__), UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER_PATH):
    os.mkdirs(UPLOAD_FOLDER_PATH)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


