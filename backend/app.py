from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)


print(os.path.abspath('instance/videos.db'))


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'instance', 'videos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploaded_videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    processing_status = db.Column(db.String(50), default='pending')

    def __repr__(self):
        return '<Video %r>' % self.title

with app.app_context():
    db.create_all()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_video = Video(title=request.form['title'], description=request.form['description'], filename=filename)
        db.session.add(new_video)
        db.session.commit()
        
        return jsonify({
            "id": new_video.id,
            "title": new_video.title,
            "description": new_video.description,
            "filename": new_video.filename
        }), 200

@app.route('/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    videos_data = [{
        "id": video.id,
        "title": video.title,
        "description": video.description,
        "filename": video.filename
    } for video in videos]
    
    return jsonify(videos_data)

if __name__ == '__main__':
    app.run(debug=True)
