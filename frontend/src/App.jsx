import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './VideoUpload.css';

const VideoUpload = () => {
  const [videos, setVideos] = useState([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    file: null
  });

  useEffect(() => {
    fetchVideos(); // Fetch videos on component mount
  }, []);

  const fetchVideos = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/videos');
      setVideos(response.data);
      console.log('Videos fetched:', response.data); // Log fetched videos
    } catch (error) {
      console.error('Error fetching videos:', error);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, file: e.target.files[0] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData();
    data.append('title', formData.title);
    data.append('description', formData.description);
    data.append('file', formData.file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
      setFormData({ title: '', description: '', file: null }); // Reset form
      fetchVideos(); // Refresh the video list
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  return (
    <div className="ui container">
      <h1 className="ui dividing header">Upload New Video</h1>
      <form className="ui form" onSubmit={handleSubmit} encType="multipart/form-data">
        <div className="field">
          <label>Title</label>
          <input type="text" name="title" placeholder="Video Title" value={formData.title} onChange={handleInputChange} />
        </div>
        <div className="field">
          <label>Description</label>
          <textarea name="description" placeholder="Video Description" value={formData.description} onChange={handleInputChange} />
        </div>
        <div className="field">
          <label>File</label>
          <input type="file" name="file" onChange={handleFileChange} />
        </div>
        <button className="ui button primary" type="submit">Upload</button>
      </form>
      <h2 className="ui dividing header">Uploaded Videos</h2>
      <div className="ui segments">
        {Array.isArray(videos) && videos.map((video) => {
          console.log('Rendering video:', video); // Log each video being rendered
          const videoSrc = `http://127.0.0.1:5000/static/uploaded_videos/${video.filename}`;
          console.log('Video source URL:', videoSrc);

          return (
            <div className="ui segment" key={video.id}>
              <h3 className="ui header">{video.title}</h3>
              <p>{video.description}</p>
              <video width="320" height="240" controls>

                <source src={`/static/uploaded_videos/${video.filename}`} type="video/quicktime" />
                Your browser does not support the video tag.
              </video>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default VideoUpload;