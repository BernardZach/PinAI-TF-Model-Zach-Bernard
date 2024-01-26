import os
from app import db, Video, app  # Importing the app, db, and Video from app.py

def cleanup():
    videos = Video.query.all()
    for video in videos:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        print(f"Checking file path: {file_path}")  # Debug: Check the file path
        
        if not os.path.exists(file_path):
            print(f"File {video.filename} not found. Deleting database record.")
            db.session.delete(video)
            try:
                db.session.commit()
                print(f"Deleted record for {video.filename}")
            except Exception as e:
                print(f"Error deleting video {video.filename} from database: {e}")
                db.session.rollback()

if __name__ == "__main__":
    with app.app_context():  # Use the existing app context
        cleanup()
