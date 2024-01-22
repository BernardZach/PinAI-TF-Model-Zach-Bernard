import os
from flask import current_app
from app import db, Video, app  # Ensure you're importing 'app' from your Flask application

# Assuming 'app' is the instance of your Flask application
with app.app_context():
    # Path to the uploaded_videos directory
    videos_path = os.path.join(current_app.root_path, 'static/uploaded_videos')

    # Get all Video records
    videos = Video.query.all()

    for video in videos:
        video_file_path = os.path.join(videos_path, video.filename)
        
        # Check if the video file exists
        if not os.path.exists(video_file_path):
            # If the file does not exist, delete the record from the database
            db.session.delete(video)
            db.session.commit()
