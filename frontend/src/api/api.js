import axios from 'axios';

// Létrehozunk egy előre beállított Axios klienst
// Ez automatikusan a Python FastAPI szerverünket fogja hívni
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
