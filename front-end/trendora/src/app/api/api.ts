import axios from 'axios';

// Create an Axios instance
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/', // Replace with your API's base URL
    timeout: 10000, // Optional: Set a timeout for requests (in milliseconds)
    headers: {
        'Content-Type': 'application/json', // Optional: Default content type
    },
    withCredentials: true
});
export default apiClient