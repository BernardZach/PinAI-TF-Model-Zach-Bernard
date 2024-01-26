import os
import sys
sys.path.append('/path/to/your/flask/app')
from app import app, db, Video

# No need to import current_app as you have the 'app' instance

with app.app_context():
    # Path to the uploaded_videos directory
    videos_path = os.path.join(app.config['UPLOAD_FOLDER'])

    # Get all Video records
    videos = Video.query.all()

    for video in videos:
        video_file_path = os.path.join(videos_path, video.filename)
        
        # Check if the video file exists
        if not os.path.exists(video_file_path):
            # If the file does not exist, delete the record from the database
            db.session.delete(video)
            print(f"Deleting {video.title} from database as file is missing.")
            db.session.commit()
