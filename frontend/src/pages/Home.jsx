import { useState, useEffect } from 'react';
import api from '../api/api';

function Home() {
    const [message, setMessage] = useState('Betöltés a backendről...');
    const [error, setError] = useState(null);

    // A komponens betöltésekor automatikusan lefutó kód (adatok lekérése a FastAPI / végpontjáról)
    useEffect(() => {
        const fetchMessage = async () => {
            try {
                const response = await api.get('/');
                setMessage(response.data.message);
            } catch (err) {
                console.error("Hiba történt a backend lekérésekor:", err);
                setError("Nem sikerült kapcsolódni a szerverhez. Ellenőrizd, hogy fut-e az uvicorn!");
            }
        };

        fetchMessage();
    }, []); // Az üres tömb [] jelenti, hogy csak legelső rendereléskor indul el.

    return (
        <div className="container" style={{ marginTop: '3rem' }}>
            <div className="main-content">
                <h1>BISEL Rendszer</h1>
                <p style={{ marginTop: '1rem', fontSize: '1.2rem', color: 'var(--color-primary)' }}>
                    {error ? <span style={{ color: 'red' }}>{error}</span> : message}
                </p>

                <div style={{ marginTop: '2rem' }}>
                    <button className="btn btn-primary" onClick={() => alert('Gomb működik!')}>
                        Teszt Gomb
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Home;
