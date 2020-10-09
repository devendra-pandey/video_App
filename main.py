import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import functools
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
datetime.utcnow()
import pymysql

ALLOWED_EXTENSIONS = ["jpg", "png", "mov", "mp4", "mpg"]

app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024 * 1024  # 1000mb

app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
## local ##
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sdp150516@localhost:3306/video_app'

db = SQLAlchemy(app)

@app.before_first_request
def createTable():
    db.create_all()
    db.session.commit()


class video_file(db.Model):
    __tablename__ = "backend_video"

    id = db.Column(db.Integer, primary_key=True)
    inserted_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    video_filename = db.Column(db.String(500), nullable=False)


class feedback(db.Model):
    __tablename__ = "backend_feedback"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer,db.ForeignKey('backend_video.id'),nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    like = db.Column(db.Boolean, default=False)



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	# data = request.get_json()
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
		new_video = video_file(video_filename=file.filename)
		db.session.add(new_video)
		db.session.commit()
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

@app.route('/get_video', methods=['GET'])
def get_video():
	video = video_file.query.filter_by(is_active="1").all()
	result = []
	for vedios in video:
		vedios_data = {}
		vedios_data['id'] = vedios.id
		vedios_data['video_filename'] = vedios.video_filename
		
		result.append(vedios_data)
		
	return jsonify({'vedios': result})

@app.route('/comments', methods=['POST'])
def feedback_video():
    data = request.get_json()
    comment_data = feedback( comment = data['comment'],video_id= data['video_id'])
    print("$$$%%^^^%$#$%^&^%$#@#$%%$#")
    db.session.add(comment_data)
    db.session.commit()

    return jsonify({'message': 'comment aaded successfull'})

@app.route('/comments_get/<video_id>', methods=['GET'])
def feedback_video():
	feedbacks = feedback.query.filter_by(video_id=video_id).first()
    result = []
	for comments in feedbacks:
		feedbacks_data = {}
		feedbacks_data['id'] = comments.id
		feedbacks_data['comment'] = comments.comment

		result.append(feedbacks_data)
		
	return jsonify({'vedios': result})
    




if __name__ == "__main__":
    app.run()