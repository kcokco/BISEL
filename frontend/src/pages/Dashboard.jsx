import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../api/api';

function Dashboard() {
    const { user } = useContext(AuthContext);
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchMyReports = async () => {
            try {
                const response = await api.get('/reports/me');
                setReports(response.data);
            } catch (err) {
                console.error('API hívási hiba részletei:', err);
                // Pontos hibaüzenet kiíratása a UI-ra a debugolás kedvéért
                if (err.response && err.response.data && err.response.data.detail) {
                    setError(`Szerver válasz: ${err.response.data.detail}`);
                } else {
                    setError(`API hiba: ${err.message || JSON.stringify(err)}`);
                }
            } finally {
                setLoading(false);
            }
        };

        fetchMyReports();
    }, []);

    return (
        <div className="container" style={{ padding: '2rem 1rem' }}>
            <h2 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#1f2937' }}>Kezelőpult</h2>
            <p style={{ fontSize: '1.1rem', color: '#4b5563', marginBottom: '2rem' }}>
                Üdvözlünk a BISEL rendszer védett felületén! Bárki, aki ezt látja, sikeresen bejelentkezett.
            </p>

            <div style={{ padding: '1.5rem', backgroundColor: '#f3f4f6', borderRadius: '12px', border: '1px solid #e5e7eb' }}>
                <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#111827' }}>A te méréseid</h3>

                {loading && <p style={{ color: '#4b5563' }}>Mérések betöltése...</p>}
                {error && <p style={{ color: '#ef4444' }}>{error}</p>}

                {!loading && !error && reports.length === 0 && (
                    <p style={{ color: '#4b5563' }}>Jelenleg nincsenek leadott méréseid.</p>
                )}

                {!loading && !error && reports.length > 0 && (
                    <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
                        {reports.map((report) => (
                            <div key={report.id} style={{ padding: '1rem', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
                                <p style={{ margin: '0 0 0.5rem 0', fontWeight: 'bold' }}>Dátum: {new Date(report.date).toLocaleDateString('hu-HU')}</p>
                                <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.9rem', color: '#4b5563' }}>Helyszín ID: {report.sampling_site_id}</p>
                                {report.bisel_index && (
                                    <p style={{ margin: '0', display: 'inline-block', backgroundColor: '#dbeafe', color: '#1d4ed8', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                                        BISEL Index: {report.bisel_index}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
