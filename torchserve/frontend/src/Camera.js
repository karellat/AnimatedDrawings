import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import CircularProgress from '@mui/material/CircularProgress';
import Button from '@mui/material/Button';
import axios from 'axios';
import { FilePicker } from "react-file-picker";

import './camera.css'; // Import the CSS file

const backendURL = process.env.REACT_APP_BACKEND_URL;
const Camera = () => {
  const webcamRef = useRef(null);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [uploading, setUploading] = useState(false);

  const capturePhoto = () => {
    const photoData = webcamRef.current.getScreenshot();
    setCapturedPhoto(photoData);
    sendPhotoToBackend(photoData);
  };

  const sendPhotoToBackend = async (photoData) => {
    try {
      const response = await axios.post('/predictions/drawn_humanoid_detector',
                       {data: photoData.split(',')[1]}, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setUploading(true);
      console.log('Uploading');
      console.log(response);
      console.log('Photo uploaded successfully!');
      setUploading(false);
    } catch (error) {
      console.error('Error uploading photo:', error);
      //setUploading(false);
      //setCapturedPhoto(null);
    }
  };

  const restartCapture = () => {
    setCapturedPhoto(null);
  };

  return (
    <div className="camera-container">
      <div className="camera-preview">
        {capturedPhoto ? (
          <>
            <img src={capturedPhoto} alt="Captured" width="100%" height="auto" />
            {uploading && (
              <div className="progress-overlay">
                <CircularProgress color="primary" size={50} />
              </div>
            )}
          </>
        ) : (
          <Webcam audio={false} ref={webcamRef} />
        )}
      </div>
      {capturedPhoto ? (
        <Button
          className="restart-button"
          variant="contained"
          color="secondary"
          size="large"
          onClick={restartCapture}
        >
          Restart
        </Button>
      ) : (<div>

        <Button
          className="capture-button"
          variant="contained"
          color="primary"
          size="large"
        >
          Capture Photo
        </Button>
        <Button>
          Add file
        </Button>
      </div>
      )}
    </div>
  );
};

export default Camera;
