import axios from 'axios';

// Létrehozunk egy előre beállított Axios klienst
// Ez automatikusan a Python FastAPI szerverünket fogja hívni
const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Axios Kérés Interceptor - Token hozzáadása
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


// Axios Válasz Interceptor - Globális Hibakezelés
api.interceptors.response.use(
    (response) => {
        // Sikeres válaszok simán továbbmennek
        return response;
    },
    (error) => {
        // Ha 401 (Jogosulatlan/Lejárt token) hibát kapunk bármilyen végpontról
        if (error.response && error.response.status === 401) {
            // Nem a login végponton vagyunk éppen (az külön kezeli a 401-et)
            if (!error.config.url.includes('/login')) {
                console.warn('Lejárt vagy érvénytelen token! Automatikus kijelentkezés.');
                // Töröljük a tokent a kliensből
                localStorage.removeItem('token');

                // Mivel react-router hook-ot itt ritkán tudunk hazsnálni (komponensen kívül), 
                // kényszerítjük az újratöltést vagy irányítást a natív window objektummal
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
