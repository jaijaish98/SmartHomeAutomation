/**
 * Camera Service
 * Handles communication with backend for camera operations
 */

import axios from 'axios';

// Backend API base URL
const API_BASE_URL = 'http://localhost:5000/api';
const STREAM_BASE_URL = 'http://localhost:5000/stream';

/**
 * Get list of available cameras
 * @returns {Promise<Array>} List of camera objects
 */
export const getAvailableCameras = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/cameras`);

    if (response.data.success) {
      return response.data.cameras;
    } else {
      throw new Error(response.data.error || 'Failed to fetch cameras');
    }
  } catch (error) {
    console.error('Error fetching cameras:', error);
    throw error;
  }
};

/**
 * Open camera stream
 * @param {number} cameraId - Camera ID to open
 * @returns {Promise<Object>} Camera stream information
 */
export const openCamera = async (cameraId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/cameras/${cameraId}/open`);
    return response.data;
  } catch (error) {
    console.error('Error opening camera:', error);
    throw error;
  }
};

/**
 * Close camera stream
 * @param {number} cameraId - Camera ID to close
 * @returns {Promise<Object>} Response object
 */
export const closeCamera = async (cameraId) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/cameras/${cameraId}/close`);
    return response.data;
  } catch (error) {
    console.error('Error closing camera:', error);
    throw error;
  }
};

/**
 * Get camera stream URL
 * @param {number} cameraId - Camera ID
 * @returns {string} Stream URL
 */
export const getCameraStreamUrl = (cameraId) => {
  return `${STREAM_BASE_URL}/${cameraId}`;
};

